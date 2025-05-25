from abc import ABC, abstractmethod
from file_storing_service.domain.entities import FileEntity


class FileRepository(ABC):
    @abstractmethod
    def find_by_hash(self, hash: str) -> FileEntity | None: ...

    @abstractmethod
    def find_by_id(self, file_id: str) -> FileEntity | None: ...

    @abstractmethod
    def add(self, entity: FileEntity) -> None: ...
