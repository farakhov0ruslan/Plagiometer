from typing import Protocol
from file_analysis_service.domain.entities import AnalysisResult


class AnalysisResultRepository(Protocol):
    def get(self, file_id: str) -> AnalysisResult | None:
        ...

    def save(self, result: AnalysisResult) -> None:
        ...
