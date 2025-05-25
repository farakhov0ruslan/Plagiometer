import requests
from fastapi import HTTPException
from config import settings


def upload_to_file_service(filename: str, content: bytes, content_type: str) -> dict:
    files = {"file": (filename, content, content_type)}
    resp = requests.post(f"{settings.FILE_SERVICE_URL}/files/", files=files)
    if not resp.ok:
        raise HTTPException(status_code=resp.status_code, detail=resp.text)
    return resp.json()


def stream_from_file_service(file_id: str):
    resp = requests.get(f"{settings.FILE_SERVICE_URL}/files/{file_id}", stream=True)
    if resp.status_code == 404:
        raise HTTPException(status_code=404, detail="File not found")
    if not resp.ok:
        raise HTTPException(status_code=resp.status_code, detail=resp.text)
    return resp


def analyze_file_via_service(file_id: str) -> dict:
    url = f"{settings.ANALYSIS_SERVICE_URL}/analysis/{file_id}"
    resp = requests.get(url)
    if resp.status_code == 404:
        raise HTTPException(status_code=404, detail="Analysis not found")
    if not resp.ok:
        raise HTTPException(status_code=resp.status_code, detail=resp.text)
    return resp.json()


def stream_wordcloud_via_service(file_id: str):
    url = f"{settings.ANALYSIS_SERVICE_URL}/analysis/wordcloud/{file_id}"
    resp = requests.get(url, stream=True)
    if resp.status_code == 404:
        raise HTTPException(status_code=404, detail="Wordcloud not found")
    if not resp.ok:
        raise HTTPException(status_code=resp.status_code, detail=resp.text)
    return resp
