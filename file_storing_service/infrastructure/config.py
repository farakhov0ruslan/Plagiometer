# api_gateway/infrastructure/config.py

from pydantic import AnyHttpUrl
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    FILE_SERVICE_URL: AnyHttpUrl
    APP_HOST: str = "0.0.0.0"
    APP_PORT: int = 80
    DATABASE_URL: str  # e.g. postgresql://user:pass@localhost:5432/files
    STORAGE_PATH: str = "./data"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
