from abc import ABC
from typing import Any

from backend.src.db.storage import AbstractStorage


class AbstractMixin(ABC):
    pass


class MixinModel(AbstractMixin):
    def __init__(self, storage: AbstractStorage):
        self.storage = storage

    async def _get_from_storage(self, collection: str,
                                data: dict) -> bytes | None:
        data = await self.storage.get_one(collection, data)
        if not data:
            return None
        return data

    async def _put_to_storage(self, collection: str, data: Any):
        await self.storage.set(collection, data)
