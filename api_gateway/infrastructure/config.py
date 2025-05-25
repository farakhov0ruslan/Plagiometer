from pydantic import BaseSettings, AnyHttpUrl


class Settings(BaseSettings):
    # URL до File Storing Service (например http://file_service:80/api)
    FILE_SERVICE_URL: AnyHttpUrl
    # Хост и порт для Uvicorn
    APP_HOST: str = "0.0.0.0"
    APP_PORT: int = 80

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
