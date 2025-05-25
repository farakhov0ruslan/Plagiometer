from abc import ABC, abstractmethod


class StorageGateway(ABC):
    """Порт для сохранения и чтения файлов."""

    @abstractmethod
    def save(self, file_id: str, content: bytes) -> str:
        """Сохранить байты file_id → вернуть путь (location)."""
        ...

    @abstractmethod
    def load(self, location: str) -> bytes:
        """Прочитать байты по указанному пути."""
        ...
