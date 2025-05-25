from fastapi import APIRouter, UploadFile, File
from starlette.responses import StreamingResponse

from file_storing_service.application.use_cases.store_file import StoreFile
from file_storing_service.application.use_cases.get_file import GetFile
from file_storing_service.infrastructure.db.file_repo import FileRepoPostgres
from file_storing_service.infrastructure.storage.fs_storage import FileSystemStorage
from file_storing_service.application.dtos import StoreFileRequest

router = APIRouter()


@router.post("/files/", response_model=dict)
def upload(file: UploadFile = File(...)):
    content = file.file.read()
    req = StoreFileRequest(name=file.filename, content=content)
    use_case = StoreFile(FileRepoPostgres(), FileSystemStorage())
    resp = use_case.execute(req)
    return {"file_id": resp.file_id, "existing": resp.existing}


@router.get("/files/{file_id}")
def download(file_id: str):
    use_case = GetFile(FileRepoPostgres(), FileSystemStorage())
    resp = use_case.execute(file_id)
    return StreamingResponse(iter([resp.content]), media_type="application/octet-stream",
                             headers={"Content-Disposition": f"attachment; filename={resp.name}"})
