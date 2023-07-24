from pydantic import BaseSettings


class TestSettings(BaseSettings):
    mongo: str = "mongo"
    mongo_port: int = 6379
    service_url: str = "http://localhost/api/v1/"


test_settings = TestSettings()
