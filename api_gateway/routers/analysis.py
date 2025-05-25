# routers/analysis.py

from fastapi import APIRouter
from fastapi.responses import StreamingResponse, JSONResponse
from schemas import AnalyzeFileResponse
from services import analyze_file_via_service, stream_wordcloud_via_service

router = APIRouter(
    prefix="/analysis",
    tags=["analysis"],
)


@router.get(
    "/{file_id}",
    response_model=AnalyzeFileResponse,
    response_class=JSONResponse,
)
def proxy_analyze(file_id: str):
    """
    Возвращает JSON-статистику: слово/абзац/топ-10 символов
    """
    result = analyze_file_via_service(file_id)
    return result


@router.get(
    "/wordcloud/{file_id}",
    response_class=StreamingResponse,
)
def proxy_wordcloud(file_id: str):
    """
    Стримит PNG-картинку облака слов
    """
    resp = stream_wordcloud_via_service(file_id)
    headers = {"Content-Disposition": resp.headers.get("Content-Disposition", "")}
    return StreamingResponse(
        resp.iter_content(chunk_size=1024),
        media_type=resp.headers.get("Content-Type", "image/png"),
        headers=headers,
    )
