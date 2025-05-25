from fastapi import HTTPException
from file_analysis_service.domain.repositories import AnalysisResultRepository


class GetWordcloudUseCase:
    def __init__(self, repo: AnalysisResultRepository):
        self.repo = repo

    def execute(self, file_id: str) -> str:
        record = self.repo.get(file_id)
        if not record:
            raise HTTPException(status_code=404, detail="Analysis not found")
        return record.image_location
