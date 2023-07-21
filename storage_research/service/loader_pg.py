import logging
import os
import random
import threading
from contextlib import contextmanager
from pathlib import Path
from typing import Any

import psycopg2
from psycopg2.extensions import connection as _connection
from psycopg2.extras import execute_values

from storage_research.service.generator import Generator
from storage_research.settings.config import PostgresConfig, pg_config
from storage_research.tools.time_decor import timing_decorator

log = logging.getLogger(__name__)


class LoaderPostgres:
    wright_dot_r = 0
    wright_dot_w = 0
    count_docs = 0
    tables = ["likes", "reviews", "bookmarks"]

    def __init__(self, generator: Generator, config: PostgresConfig):
        self.config = config
        self.wright_interval = config.pg_interval
        self.generator = generator
        self.db: _connection | None = None

    def _connect(self):
        return psycopg2.connect(
            dbname=self.config.pg_dbname,
            user=self.config.pg_user,
            password=self.config.pg_password,
            host=self.config.pg_host,
            port=self.config.pg_port,
        )

    @contextmanager
    def conn_context_pg(self):
        conn = self._connect()
        psycopg2.extras.register_uuid()
        yield conn
        conn.close()

    def _clear_base(self):
        with self.db.cursor() as cursor:
            for table in self.tables:
                query = f"DELETE FROM test.{table}"
                cursor.execute(query)
            self.db.commit()

    @staticmethod
    def _clear_result(path: Path):
        try:
            os.remove(path)
        except FileNotFoundError:
            pass

    def infinity_load(self):
        with self.conn_context_pg() as db:
            psycopg2.extras.register_uuid()
            for docs in self.generator.harvest():
                count = self._load_to_pg(docs, db)
                self.count_docs = count
                try:
                    if count > self.config.pg_max_docs:
                        break
                except TypeError:
                    pass

    def infinity_read(self):
        with psycopg2.connect(
            dbname=self.config.pg_dbname,
            user=self.config.pg_user,
            password=self.config.pg_password,
            host=self.config.pg_host,
            port=self.config.pg_port,
        ) as db:
            psycopg2.extras.register_uuid()
            while True:
                self._read_pg(db)
                try:
                    if self.generator.counter > self.config.pg_max_docs:
                        break
                except TypeError:
                    pass

    @timing_decorator("Запись PG", pg_config.pg_result_w)
    def _load_to_pg(self, docs: list[Any], db):
        with db.cursor() as cursor:
            columns = docs[0].model_dump(by_alias=True, exclude={"collection"}).keys()
            values = [
                list(doc.model_dump(by_alias=True, exclude={"collection"}).values())
                for doc in docs
            ]
            query = f"INSERT INTO test.{docs[0].collection} ({', '.join(columns)}) VALUES %s"
            execute_values(cursor, query, values)
            db.commit()
            self.wright_dot_w += 1
            if self.wright_dot_w == self.wright_interval:
                self.wright_dot_w = 0
                return self.generator.counter
            else:
                return None

    @timing_decorator("Чтение PG", pg_config.pg_result_r)
    def _read_pg(self, db):
        with db.cursor() as cursor:
            query = f"SELECT * FROM test.{self.tables[random.randint(0, 2)]} ORDER BY RANDOM() LIMIT 10"
            cursor.execute(query)
            t = cursor.fetchall()
        return self.generator.counter

    def run(self):
        write_thread = threading.Thread(target=self.infinity_load)
        read_thread = threading.Thread(target=self.infinity_read)
        write_thread.start()
        read_thread.start()
        write_thread.join()
        read_thread.join()

    def __enter__(self):
        self.db = self._connect()
        self._clear_base()
        self._clear_result(self.config.pg_result_w)
        self._clear_result(self.config.pg_result_r)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._clear_base()
        self.db.close()
