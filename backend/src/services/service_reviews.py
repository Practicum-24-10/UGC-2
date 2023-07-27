import logging
from functools import lru_cache
from uuid import UUID

from bson import ObjectId
from fastapi import Depends

from backend.src.db.mongo_db import get_mongo
from backend.src.db.storage import AbstractStorage
from backend.src.services.mixin import MixinModel

log = logging.getLogger(__name__)


class ReviewsService(MixinModel):
    async def add_review(self, user_id: str, review: dict):
        review["user_id"] = user_id
        set_review = await self._put_to_storage('reviews', review)
        return set_review

    async def change_review(self, review_id: ObjectId, review: str):
        update_review = await self._update_to_storage('reviews',
                                                      {'review': review},
                                                      review_id)
        if update_review is not None and update_review.modified_count > 0:
            return True
        return False

    async def get_reviews(self, film_id: str, size: int, page: int):
        data = {
            "film_id": film_id
        }
        _to = size
        _from = size * (page - 1)
        result = await self._get_from_pagination('reviews', data, _from, _to)
        if result:
            return result

    async def del_review(self, review_id: ObjectId):
        data = {
            "_id": review_id
        }
        del_result = await self._del_to_storage('reviews', data)
        if del_result is not None and del_result.deleted_count > 0:
            return True
        return False

    async def get_review(self, user_id: UUID, film_id: UUID):
        data = {
            "user_id": str(user_id),
            "film_id": str(film_id)
        }
        search_review = await self._get_from_storage('reviews', data)
        if search_review is None:
            return None
        return search_review


@lru_cache()
def get_reviews_service(
        mongo: AbstractStorage = Depends(get_mongo),
) -> ReviewsService:
    return ReviewsService(mongo)
