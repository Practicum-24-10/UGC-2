from abc import ABC
from typing import Any

from bson import ObjectId

from backend.src.db.storage import AbstractStorage


class AbstractMixin(ABC):
    pass


class MixinModel(AbstractMixin):
    def __init__(self, storage: AbstractStorage):
        self.storage = storage

    async def _get_from_storage(self, collection: str,
                                data: dict):
        response = await self.storage.get_one(collection, data)
        if not response:
            return None
        return response

    async def _get_from_pagination(self, collection: str,
                                   data: dict, _from: int, _to: int) -> list | None:
        response = await self.storage.find_by_pagination(collection, data,
                                                         _from, _to)
        if not response:
            return None
        return response

    async def _update_to_storage(self, collection: str,
                                 data: dict, doc_id: ObjectId):
        response = await self.storage.update_one(collection, data, doc_id)
        if not response:
            return None
        return response

    async def _put_to_storage(self, collection: str, data: Any):
        return await self.storage.set(collection, data)

    async def _count_to_storage(self, collection: str, data: dict):
        response = await self.storage.count(collection, data)
        if not response:
            return 0
        return response

    async def _del_to_storage(self, collection: str, data: dict):
        return await self.storage.delete_one(collection, data)
