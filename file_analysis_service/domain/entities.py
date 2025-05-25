from datetime import datetime
from typing import List


class AnalysisResult:
    def __init__(
        self,
        file_id: str,
        word_count: int,
        paragraph_count: int,
        top_chars: List[str],
        image_location: str,
        created_at: datetime | None = None,
    ):
        self.file_id = file_id
        self.word_count = word_count
        self.paragraph_count = paragraph_count
        self.top_chars = top_chars
        self.image_location = image_location
        self.created_at = created_at or datetime.utcnow()
