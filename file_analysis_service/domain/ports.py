from typing import Protocol


class FileStoragePort(Protocol):
    def get_file(self, file_id: str) -> bytes:
        ...

    def store_file(self, filename: str, content: bytes, content_type: str) -> str:
        """Возвращает `location` загруженного файла."""
        ...


class WordCloudPort(Protocol):
    def generate(self, text: str) -> bytes:
        """Возвращает PNG-байты облака слов."""
        ...
