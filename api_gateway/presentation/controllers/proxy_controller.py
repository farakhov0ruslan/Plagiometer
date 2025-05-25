import json
from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import StreamingResponse, JSONResponse
from api_gateway.application.dtos import ProxyRequestDTO
from api_gateway.application.use_cases.proxy_request import ProxyRequest
from api_gateway.infrastructure.clients.http_client import HTTPClient

router = APIRouter()
_http_client = HTTPClient()
_proxy_uc = ProxyRequest(_http_client)


@router.post("/api/files/", response_class=JSONResponse)
async def proxy_upload(file: UploadFile = File(...)):
    # Читаем файл в память
    content = await file.read()
    # Формируем DTO
    req = ProxyRequestDTO(
        method="POST",
        path="files/",
        headers={"content-type": file.content_type},
        content=content
    )
    try:
        resp = _proxy_uc.execute(req)
    except Exception as e:
        raise HTTPException(status_code=502, detail=str(e))
    # Парсим JSON из байт и возвращаем его клиенту
    try:
        data = json.loads(resp.content)
    except json.JSONDecodeError:
        raise HTTPException(status_code=502, detail="Bad JSON from file service")
    return JSONResponse(status_code=resp.status_code, content=data)


@router.get("/api/files/{file_id}")
def proxy_download(file_id: str):
    # Формируем DTO
    req = ProxyRequestDTO(
        method="GET",
        path=f"files/{file_id}",
        headers={},
        content=b""
    )
    try:
        resp = _proxy_uc.execute(req)
    except Exception as e:
        raise HTTPException(status_code=502, detail=str(e))
    # Если файл не найден — пробросим статус
    if resp.status_code != 200:
        raise HTTPException(status_code=resp.status_code, detail=resp.content.decode("utf-8"))
    # Стримим байты обратно клиенту
    return StreamingResponse(
        iter([resp.content]),
        media_type=resp.headers.get("content-type", "application/octet-stream"),
        headers={"Content-Disposition": resp.headers.get("content-disposition", "")}
    )
