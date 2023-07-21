import logging
import os
from pathlib import Path

from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).resolve().parent.parent
RESULT_DIR = BASE_DIR.joinpath('results')
if not os.path.exists(RESULT_DIR):
    os.makedirs(RESULT_DIR)


class MongoConfig(BaseSettings):
    mongo_host: str = 'localhost'
    mongo_port: int = 27017
    mongo_interval: int = 10
    mongo_sample_size: int = 10
    mongo_max_docs: int = 1000000
    mongo_result_w: Path = RESULT_DIR.joinpath('mongo_result_w.csv')
    mongo_result_r: Path = RESULT_DIR.joinpath('mongo_result_r.csv')


class PostgresConfig(BaseSettings):
    pg_dbname: str = 'movies'
    pg_user: str = 'app'
    pg_password: str = '123qwe'
    pg_host: str = 'localhost'
    pg_port: str = '5432'
    pg_interval: int = 10
    pg_sample_size: int = 10
    pg_max_docs: int = 1000000
    pg_result_w: Path = RESULT_DIR.joinpath('pg_result_w.csv')
    pg_result_r: Path = RESULT_DIR.joinpath('pg_result_r.csv')


mongo_config = MongoConfig()
pg_config = PostgresConfig()

LOGGING = {
    "format": "%(levelname)-8s [%(asctime)s] "
              "%(name)s.%(funcName)s:%(lineno)d %(message)s",
    "level": logging.INFO,
    "handlers": [logging.StreamHandler()],
}
