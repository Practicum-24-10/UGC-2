import logging

import sentry_sdk
import uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from sentry_sdk.integrations.fastapi import FastApiIntegration

from backend.src.api.v1 import api_likes, api_reviews
from backend.src.api.v1.api_bookmarks import router as bookmarks_router
from backend.src.auth import rsa_key
from backend.src.auth.abc_key import RsaKey
from backend.src.core.config import DSN, PUBLIC_KEY, config
from backend.src.core.logger import LOGGING
from backend.src.db import mongo_db
from backend.src.db.storage import MongoStorage


if config.logging_on:
    sentry_sdk.init(dsn=DSN, integrations=[FastApiIntegration()])

    logging.basicConfig(**LOGGING)
    log = logging.getLogger(__name__)

app = FastAPI(
    title=config.project_name,
    docs_url="/api/openapi",
    openapi_url="/api/openapi.json",
    default_response_class=ORJSONResponse,
)


@app.on_event("startup")
async def startup():
    mongo_db.mongo = MongoStorage(host=config.mongo_host, port=config.mongo_port)
    rsa_key.pk = RsaKey(path=PUBLIC_KEY, algorithms=["RS256"])


@app.on_event("shutdown")
async def shutdown():
    if mongo_db.mongo:
        await mongo_db.mongo.close()


app.include_router(api_reviews.router, prefix="/api/v1/reviews", tags=["reviews"])

app.include_router(api_likes.router, prefix="/api/v1/likes", tags=["likes"])

app.include_router(bookmarks_router, prefix="/api/v1/bookmarks", tags=["bookmarks"])

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
