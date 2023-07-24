from abc import ABC, abstractmethod


class AbstractStorage(ABC):
    @abstractmethod
    async def get(self, _id: str):
        pass

    @abstractmethod
    async def set(self, _id: str, data: str):
        pass

    @abstractmethod
    async def close(self):
        pass


class MongoStorage(AbstractStorage):
    def __init__(self, host: str, port: int):
        self._connect = ...

    async def get(self, _id: str):
        pass

    async def set(self, _id: str, data: str):
        pass

    async def close(self):
        pass
