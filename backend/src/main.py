import logging
import sentry_sdk
import uvicorn

from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from sentry_sdk.integrations.fastapi import FastApiIntegration

from backend.src.api.v1 import api_likes
from backend.src.auth import rsa_key
from backend.src.auth.abc_key import RsaKey
from backend.src.core.config import PUBLIC_KEY, AppSettings, DSN
from backend.src.core.logger import LOGGING
from backend.src.db import mongo_db
from backend.src.db.storage import MongoStorage

sentry_sdk.init(
    dsn=DSN,
    integrations=[FastApiIntegration()]
)


config = AppSettings()
app = FastAPI(
    title=config.project_name,
    docs_url="/api/openapi",
    openapi_url="/api/openapi.json",
    default_response_class=ORJSONResponse,
)


@app.on_event("startup")
async def startup():
    mongo_db.mongo = MongoStorage(
        host=config.mongo_host, port=config.mongo_port)
    rsa_key.pk = RsaKey(path=PUBLIC_KEY, algorithms=["RS256"])


@app.on_event("shutdown")
async def shutdown():
    if mongo_db.mongo:
        await mongo_db.mongo.close()  # type: ignore


app.include_router(
    api_likes.router, prefix="/api/v1/likes", tags=["likes"])

if __name__ == "__main__":
    logging.basicConfig(**LOGGING)
    log = logging.getLogger(__name__)
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
