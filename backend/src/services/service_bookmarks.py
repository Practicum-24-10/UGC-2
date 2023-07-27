import logging
from functools import lru_cache
from typing import Iterable
from uuid import UUID

from backend.src.db.storage import AbstractStorage
from backend.src.db.mongo_db import get_mongo
from fastapi import Depends

from backend.src.services.mixin import MixinModel

log = logging.getLogger(__name__)


class BookmarksService(MixinModel):
    async def add_bookmarks(self, user_id: str, bookmarks: dict):
        bookmarks['user_id'] = user_id
        set_bookmarks = await self._put_to_storage('bookmarks', bookmarks)
        return set_bookmarks

    async def delete_bookmarks(self, user_id: str, bookmarks: dict):
        bookmarks['user_id'] = user_id
        del_result = await self._del_to_storage('bookmarks', bookmarks)
        if del_result is not None and del_result.deleted_count > 0:
            return True
        return False

    async def get_all_bookmarks(self, user_id: UUID) -> Iterable | None:
        data = {"user_id": str(user_id)}
        search_all_bookmarks = await self._get_all_from_storage('bookmarks', data)
        if search_all_bookmarks is None:
            return None
        return search_all_bookmarks


@lru_cache()
def get_bookmarks_service(
        mongo: AbstractStorage = Depends(get_mongo),
) -> BookmarksService:
    return BookmarksService(mongo)
