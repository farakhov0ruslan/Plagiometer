import requests
from requests import HTTPError, RequestException

from fastapi import HTTPException

from file_analysis_service.config import settings


class WordCloudClient:
    def __init__(self):
        self.base_url = settings.WORDCLOUD_API_URL.rstrip('/')

    def generate(self, text: str) -> bytes:
        params = {
            "text": text,
            "format": "png",
            "width": 800,
            "height": 400,
        }
        try:
            resp = requests.get(self.base_url, params=params, timeout=10)
            resp.raise_for_status()
        except HTTPError:
            if resp.status_code == 414:
                raise HTTPException(
                    status_code=413,
                    detail="Слишком большой объём текста для генерации облака. "
                           "Попробуйте загрузить меньший файл или сократить текст."
                )
            # все остальные 4xx/5xx — преобразуем в 502
            raise HTTPException(
                status_code=502,
                detail=f"Сервис генерации облака слов вернул {resp.status_code}"
            )
        except RequestException:
            # сетевые ошибки
            raise HTTPException(
                status_code=503,
                detail="Не удалось подключиться к сервису генерации облака слов. Попробуйте позже."
            )

        return resp.content
