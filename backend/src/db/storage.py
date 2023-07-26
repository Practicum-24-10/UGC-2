from abc import ABC, abstractmethod
from typing import Any
from bson.objectid import ObjectId

import motor.motor_asyncio


class AbstractStorage(ABC):
    @abstractmethod
    async def get_all(self, collection: str, data: dict):
        pass

    @abstractmethod
    async def find_by_pagination(self, collection: str,
                                 data: dict, skip: int, limit: int):
        pass

    @abstractmethod
    async def get_one(self, collection: str, data: dict):
        pass

    @abstractmethod
    async def delete_one(self, collection: str, data: dict):
        pass

    @abstractmethod
    async def update_one(self, collection: str, data: dict, doc_id: ObjectId):
        pass

    @abstractmethod
    async def delete_many(self, collection: str, data: dict):
        pass

    @abstractmethod
    async def count(self, collection: str, data: dict):
        pass

    @abstractmethod
    async def set(self, collection: str, model: Any):
        pass

    @abstractmethod
    async def close(self):
        pass


class MongoStorage(AbstractStorage):
    def __init__(self, host: str, port: int):
        self._connect = motor.motor_asyncio.AsyncIOMotorClient(
            f"mongodb://{host}:{port}", uuidRepresentation="standard"
        )["movies"]

    async def get_all(self, collection: str, data: dict):
        return await self._connect[collection].find(data)

    async def get_one(self, collection: str, data: dict):
        return await self._connect[collection].find_one(data)

    async def update_one(self, collection: str, data: dict, doc_id: ObjectId):
        result = await self._connect[collection].update_one({"_id": doc_id},
                                                            {"$set": data},
                                                            upsert=False)
        return result

    async def find_by_pagination(self, collection: str,
                                 data: dict, skip: int, limit: int):
        result = await self._connect[collection].find(data).skip(skip).limit(limit).to_list(None)
        return result

    async def delete_one(self, collection: str, data: dict):
        return await self._connect[collection].delete_one(data)

    async def delete_many(self, collection: str, data: dict):
        return await self._connect[collection].delete_many(data)

    async def count(self, collection: str, data: dict):
        count_result = await self._connect[collection].count_documents(data)
        return count_result

    async def set(self, collection: str, data: dict):
        new_like = await self._connect[collection].update_one(
            data, {"$setOnInsert": data}, upsert=True
        )
        return new_like.upserted_id

    async def close(self):
        pass
