import logging
import os
import random
from pathlib import Path
from typing import Any
import threading

from pymongo import MongoClient

from storage_research.service.generator import Generator

from storage_research.settings.config import MongoConfig, mongo_config
from storage_research.tools.time_decor import timing_decorator

log = logging.getLogger(__name__)
event1 = threading.Event()
event2 = threading.Event()


class LoaderMongo:
    wright_dot_r = 0
    wright_dot_w = 0
    count_docs = 0
    collections = ['likes', 'reviews', 'bookmarks']

    def __init__(self, generator: Generator, config: MongoConfig):
        self.config = config
        self.wright_interval = config.mongo_interval
        self.generator = generator
        self.db: MongoClient | None = None

    def _connect(self):
        self.db = MongoClient(
            host=self.config.mongo_host,
            port=self.config.mongo_port,
            uuidRepresentation='standard'
        )['movies']

    def _clear_base(self):
        for collection in self.collections:
            self.db[collection].delete_many({})

    @staticmethod
    def _clear_result(path: Path):
        try:
            os.remove(path)
        except FileNotFoundError:
            pass

    def infinity_load(self):
        for docs in self.generator.harvest():
            count = self._load_to_mongo(docs)
            try:
                if count > self.config.mongo_max_docs:
                    break
            except TypeError:
                pass

    def infinity_read(self):
        while True:
            self._read_mongo()
            try:
                if self.generator.counter > self.config.mongo_max_docs:
                    break
            except TypeError:
                pass

    @timing_decorator('Запись Mongo', mongo_config.mongo_result_w)
    def _load_to_mongo(self, docs: list[Any]):
        if len(docs) == 1:
            self.db[docs[0].collection].insert_one(
                docs[0].model_dump(by_alias=True, exclude={'collection'}))
        else:
            self.db[docs[0].collection].insert_many(
                [doc.model_dump(by_alias=True, exclude={'collection'}) for
                 doc in docs])
        self.wright_dot_w += 1
        if self.wright_dot_w == self.wright_interval:
            self.wright_dot_w = 0
            return self.generator.counter
        else:
            return None

    @timing_decorator('Чтение Mongo', mongo_config.mongo_result_r)
    def _read_mongo(self):
        pipeline = [{'$sample': {'size': self.config.mongo_sample_size}}]

        self.db[self.collections[random.randint(0, 2)]].aggregate(pipeline)
        return self.generator.counter

    def run(self):
        write_thread = threading.Thread(target=self.infinity_load)
        read_thread = threading.Thread(target=self.infinity_read)
        write_thread.start()
        read_thread.start()
        write_thread.join()
        read_thread.join()

    def __enter__(self):
        self._connect()
        self._clear_base()
        self._clear_result(self.config.mongo_result_w)
        self._clear_result(self.config.mongo_result_r)

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._clear_base()
