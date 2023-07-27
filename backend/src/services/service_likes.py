import logging
from functools import lru_cache
from uuid import UUID

from fastapi import Depends

from backend.src.db.mongo_db import get_mongo
from backend.src.db.storage import AbstractStorage
from backend.src.services.mixin import MixinModel

log = logging.getLogger(__name__)


class LikeService(MixinModel):
    async def add_like(self, user_id: str, like: dict):
        like["user_id"] = user_id
        set_like = await self._put_to_storage('likes', like)
        return set_like

    async def dell_like(self, like_id: str):
        data = {
            "_id": like_id
        }
        del_result = await self._del_to_storage('likes', data)
        if del_result:
            return del_result.acknowledged

    async def get_count(self, film_id: UUID):
        data = {
            "film_id": str(film_id),
            "value": 1
        }
        likes = await self._count_to_storage('likes', data)
        data["value"] = 0
        dislike = await self._count_to_storage('likes', data)
        return likes, dislike

    async def get_like(self, user_id: UUID, film_id: UUID):
        data = {
            "user_id": str(user_id),
            "film_id": str(film_id)
        }
        search_like = await self._get_from_storage('likes', data)
        if search_like is None:
            return None
        return search_like


@lru_cache()
def get_like_service(
        mongo: AbstractStorage = Depends(get_mongo),
) -> LikeService:
    return LikeService(mongo)
