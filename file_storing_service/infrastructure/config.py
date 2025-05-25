# file_storing_service/infrastructure/config.py
import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # URL для подключения к БД
    DATABASE_URL: str
    # Куда сохранять файлы на диске
    STORAGE_PATH: str = "./data"

    class Config:
        # файл с переменными окружения лежит рядом с этим модулем

        env_file = os.path.join("file_storing_service", ".env")
        env_file_encoding = "utf-8"

# единственный экземпляр настроек
settings = Settings()

