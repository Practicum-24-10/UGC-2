import os
from logging import config as logging_config

import dotenv
from pydantic import BaseSettings

from backend.src.core.logger import LOGGING

dotenv.load_dotenv()


class AppSettings(BaseSettings):
    project_name: str = "Some project name"
    mongo_host: str = "localhost"
    mongo_port: int = 27017
    logging_on: bool = True


config = AppSettings()

if config.logging_on:
    logging_config.dictConfig(LOGGING)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

PUBLIC_KEY_DIR = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    )  # type: ignore

PUBLIC_KEY = os.path.join(PUBLIC_KEY_DIR, os.environ.get("PUBLIC_KEY"))  # type: ignore

DSN = os.environ.get('SENTRY_DSN')
