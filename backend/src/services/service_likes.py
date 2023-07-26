import logging
from functools import lru_cache
from uuid import UUID

from backend.src.db.storage import AbstractStorage
from backend.src.db.mongo_db import get_mongo
from fastapi import Depends

from backend.src.models.model_likes import Like
from backend.src.services.mixin import MixinModel

log = logging.getLogger(__name__)


class LikeService(MixinModel):
    async def add_like(self, user_id: str, like: Like):
        set_like = await self._put_to_storage('likes', user_id, like)
        return set_like

    async def dell_like(self, like_id: str):
        del_result = await self._del_to_storage('likes', like_id)
        if del_result:
            return del_result.acknowledged

    async def get_like(self, user_id: UUID, film_id: UUID):
        data = {
            "user_id": str(user_id),
            "film_id": str(film_id)
        }
        search_like = await self._get_from_storage('likes', data)
        if search_like is None:
            return None
        return search_like['_id']


@lru_cache()
def get_like_service(
        mongo: AbstractStorage = Depends(get_mongo),
) -> LikeService:
    return LikeService(mongo)
