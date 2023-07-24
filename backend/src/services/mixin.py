from abc import ABC

from backend.src.db.storage import AbstractStorage


class AbstractMixin(ABC):
    pass


class MixinModel(AbstractMixin):
    def __init__(self, storage: AbstractStorage):
        self.storage = storage

    async def _get_from_storage(self, _id: str) -> bytes | None:
        data = await self.storage.get(_id)
        if not data:
            return None
        return data

    async def _put_to_storage(self, _id: str, data: str):
        await self.storage.set(_id, data)
