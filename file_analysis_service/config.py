import os


class Settings:
    # URL вашего File Storing Service
    FILE_SERVICE_URL: str = os.getenv("FILE_SERVICE_URL", "http://file_service:80")
    # URL WordCloud API и ключ
    WORDCLOUD_API_URL: str = os.getenv("WORDCLOUD_API_URL", "https://wordcloudapi.com/api/v1")
    WORDCLOUD_API_KEY: str = os.getenv("WORDCLOUD_API_KEY", "")
    # URL базы для анализа
    DATABASE_URL: str = os.getenv("DATABASE_URL",
                                  "postgresql://user:pass@file_analysis_db:5432/analysis")


settings = Settings()
