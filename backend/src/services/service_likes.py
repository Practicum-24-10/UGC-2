import logging
from functools import lru_cache
from uuid import UUID

from backend.src.db.storage import AbstractStorage
from backend.src.db.mongo_db import get_mongo
from fastapi import Depends

from backend.src.services.mixin import MixinModel

log = logging.getLogger(__name__)


class LikeService(MixinModel):
    async def add_like(self, user_id: UUID, film_id: UUID, rating: int):
        pass

    async def get_like(self, user_id: UUID, film_id: UUID):
        pass


@lru_cache()
def like_service(
        mongo: AbstractStorage = Depends(get_mongo),
) -> LikeService:
    return LikeService(mongo)
