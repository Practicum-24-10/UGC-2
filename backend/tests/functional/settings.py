from pydantic import BaseSettings


class TestSettings(BaseSettings):
    mongo_host: str = "localhost"
    mongo_port: int = 27017
    service_url: str = "http://localhost/api/v1/"


test_settings = TestSettings()
