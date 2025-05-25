import os


class Settings:
    FILE_SERVICE_URL: str = os.getenv("FILE_SERVICE_URL", "http://file_service:80")
    ANALYSIS_SERVICE_URL: str = os.getenv("ANALYSIS_SERVICE_URL", "http://file_analysis_service:80")


settings = Settings()
