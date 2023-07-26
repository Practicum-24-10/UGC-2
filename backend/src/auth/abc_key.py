from abc import ABC, abstractmethod


class AbstractKey(ABC):
    key: str | None
    algorithms: list[str] | None
    pl_is_superuser: str | None
    pl_permissions: str | None
    pl_sub: str | None

    @abstractmethod
    async def _load(self, path: str):
        pass


class RsaKey(AbstractKey):
    key: str | None
    algorithms: list[str] | None
    pl_is_superuser: str | None
    pl_permissions: str | None
    pl_sub: str | None

    def __init__(self, path: str, algorithms: list[str]):
        self._load(path)
        self.algorithms = algorithms
        self.pl_permissions = 'permissions'
        self.pl_is_superuser = 'is_superuser'
        self.pl_sub = 'sub'

    def _load(self, path: str):
        self.key = open(path).read()
