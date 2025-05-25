# file_analysis_service/infrastructure/file_storage_client.py
import requests
from fastapi import HTTPException
from requests import RequestException

class FileStorageClient:
    def __init__(self, base_url: str):
        self.base = base_url.rstrip('/')

    def get_file(self, file_id: str) -> bytes:
        try:
            resp = requests.get(f"{self.base}/files/{file_id}", stream=True, timeout=5)
        except RequestException:
            # любая сетевуха — отдаём 503
            raise HTTPException(
                status_code=503,
                detail="Сервис хранения файлов недоступен. Попробуйте позже."
            )

        if resp.status_code == 404:
            raise HTTPException(status_code=404, detail="Файл не найден")
        if 500 <= resp.status_code < 600:
            raise HTTPException(
                status_code=503,
                detail=f"Сервис хранения вернул {resp.status_code}"
            )
        resp.raise_for_status()
        return resp.content

    def store_file(self, filename: str, content: bytes, content_type: str) -> str:
        files = {"file": (filename, content, content_type)}
        try:
            resp = requests.post(f"{self.base}/files/", files=files, timeout=5)
        except RequestException:
            raise HTTPException(
                status_code=503,
                detail="Сервис хранения файлов недоступен. Попробуйте позже."
            )

        if resp.status_code == 409:
            # 409 — файл уже есть, получаем URL из ответа
            return resp.json().get("location")
        if 500 <= resp.status_code < 600:
            raise HTTPException(
                status_code=503,
                detail=f"Сервис хранения вернул {resp.status_code}"
            )
        resp.raise_for_status()
        return resp.json()["location"]
