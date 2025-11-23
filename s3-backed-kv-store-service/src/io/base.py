from abc import ABC, abstractmethod

class BaseClient(ABC):
    @abstractmethod
    def get_object(self, key: str) -> bytes:
        pass

    @abstractmethod
    def put_object(self, key: str, value: bytes) -> None:
        pass