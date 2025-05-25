from fastapi import APIRouter, UploadFile, File
from fastapi.responses import StreamingResponse
from schemas import UploadResponse
from services import upload_to_file_service, stream_from_file_service

router = APIRouter(
    prefix="/api/files",
    tags=["files"],
)


@router.post("/", response_model=UploadResponse)
async def upload_file(file: UploadFile = File(...)):
    """
       Загрузить файл в системку
    """
    content = await file.read()
    result = upload_to_file_service(file.filename, content, file.content_type)
    return result


@router.get("/{file_id}")
def download_file(file_id: str):
    """
           Получать файл из системы по id
    """
    resp = stream_from_file_service(file_id)
    headers = {"Content-Disposition": resp.headers.get("Content-Disposition", "")}
    return StreamingResponse(
        resp.iter_content(chunk_size=1024),
        media_type=resp.headers.get("content-type", "application/octet-stream"),
        headers=headers
    )
