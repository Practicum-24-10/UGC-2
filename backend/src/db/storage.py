from abc import ABC, abstractmethod
from typing import Any

import motor.motor_asyncio


class AbstractStorage(ABC):
    @abstractmethod
    async def get_all(self, collection: str, data: dict):
        pass

    @abstractmethod
    async def get_one(self, collection: str, data: dict):
        pass

    @abstractmethod
    async def delete_one(self, collection: str, data: dict):
        pass

    @abstractmethod
    async def delete_many(self, collection: str, data: dict):
        pass

    @abstractmethod
    async def set(self, collection: str, model: Any):
        pass

    @abstractmethod
    async def close(self):
        pass


class MongoStorage(AbstractStorage):
    def __init__(self, host: str, port: int):
        self._connect = \
        motor.motor_asyncio.AsyncIOMotorClient(f'mongodb://{host}:{port}',
                                               uuidRepresentation="standard")[
            'movies']

    async def get_all(self, collection: str, data: dict):
        return await self._connect[collection].find(data)

    async def get_one(self, collection: str, data: dict):
        return await self._connect[collection].find_one(data)

    async def delete_one(self, collection: str, data: dict):
        return await self._connect[collection].delete_one(data)

    async def delete_many(self, collection: str, data: dict):
        return await self._connect[collection].delete_many(data)

    async def set(self, collection: str, data: dict):
        new_like = await self._connect[collection].update_one(data, {
            "$setOnInsert": data
        }, upsert=True)
        return new_like.upserted_id

    async def close(self):
        pass
