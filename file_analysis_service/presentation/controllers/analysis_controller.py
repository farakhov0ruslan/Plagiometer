# file_analysis_service/presentation/controllers/analysis_controller.py
from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse, FileResponse
from sqlalchemy.orm import Session
from file_analysis_service.infrastructure.db.database import get_db
from file_analysis_service.infrastructure.db.repositories import SqlAlchemyAnalysisResultRepo
from file_analysis_service.infrastructure.file_storage_client import FileStorageClient
from file_analysis_service.infrastructure.wordcloud_client import WordCloudClient
from file_analysis_service.infrastructure.local_storage import LocalStorage
from file_analysis_service.application.use_cases.analyze_file import AnalyzeFileUseCase
from file_analysis_service.application.use_cases.get_wordcloud import GetWordcloudUseCase
from file_analysis_service.application.dto import AnalyzeFileRequest, AnalyzeFileResponse
import os

router = APIRouter()


@router.get(
    "/analysis/{file_id}",
    response_model=AnalyzeFileResponse,
    response_class=JSONResponse,
    tags=["analysis"]
)
def analyze(file_id: str, db: Session = Depends(get_db)):
    repo    = SqlAlchemyAnalysisResultRepo(db)
    storage = FileStorageClient(base_url=os.getenv("FILE_SERVICE_URL"))
    wc      = WordCloudClient()
    local   = LocalStorage(base_dir="data")
    uc      = AnalyzeFileUseCase(repo, storage, wc, local)

    # все HTTPException (404/503/…) уже выброшены в client/use_case
    return uc.execute(AnalyzeFileRequest(file_id=file_id))


@router.get(
    "/analysis/wordcloud/{file_id}",
    response_class=FileResponse,
    tags=["analysis"]
)
def get_cloud(file_id: str, db: Session = Depends(get_db)):
    repo = SqlAlchemyAnalysisResultRepo(db)
    uc   = GetWordcloudUseCase(repo)

    path = uc.execute(file_id)  # HTTPException(404) если нет записи
    if not os.path.isfile(path):
        raise HTTPException(status_code=404, detail="Картинка не найдена на диске")
    return FileResponse(path, media_type="image/png", filename=os.path.basename(path))
