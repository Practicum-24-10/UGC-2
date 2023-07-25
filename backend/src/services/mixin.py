from abc import ABC
from typing import Any

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

    async def _put_to_storage(self, collection: str, user_id: str, data: Any):
        data["user_id"] = user_id
        return await self.storage.set(collection, data)

    async def _del_to_storage(self, collection: str, like_id: str):
        data = {
            "_id": like_id
        }
        return await self.storage.delete_one(collection,data)
