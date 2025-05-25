import os
from file_storing_service.application.ports.storage_port import StorageGateway
from file_storing_service.infrastructure.config import settings


class FileSystemStorage(StorageGateway):
    """
    Хранит файлы на локальном диске в папке settings.STORAGE_PATH.
    """

    def save(self, file_id: str, content: bytes) -> str:
        # Убедимся, что папка существует
        os.makedirs(settings.STORAGE_PATH, exist_ok=True)
        # Путь вида "./data/<file_id>"
        path = os.path.join(settings.STORAGE_PATH, file_id)
        # Запишем файл
        with open(path, "wb") as f:
            f.write(content)
        return path

    def load(self, location: str) -> bytes:
        # Прочитаем и вернём байты
        with open(location, "rb") as f:
            return f.read()
