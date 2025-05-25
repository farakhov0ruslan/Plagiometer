from sqlalchemy.orm import Session
from file_analysis_service.domain.entities import AnalysisResult
from file_analysis_service.domain.repositories import AnalysisResultRepository
from file_analysis_service.infrastructure.db.models import AnalysisResultModel


class SqlAlchemyAnalysisResultRepo(AnalysisResultRepository):
    def __init__(self, db: Session):
        self.db = db

    def get(self, file_id: str) -> AnalysisResult | None:
        m = self.db.get(AnalysisResultModel, file_id)
        if not m:
            return None
        return AnalysisResult(
            file_id=m.file_id,
            word_count=m.word_count,
            paragraph_count=m.paragraph_count,
            top_chars=m.top_chars,
            image_location=m.image_location,
            created_at=m.created_at,
        )

    def save(self, result: AnalysisResult) -> None:
        m = AnalysisResultModel(
            file_id=result.file_id,
            word_count=result.word_count,
            paragraph_count=result.paragraph_count,
            top_chars=result.top_chars,
            image_location=result.image_location,
            created_at=result.created_at,
        )
        self.db.add(m)
        self.db.commit()
