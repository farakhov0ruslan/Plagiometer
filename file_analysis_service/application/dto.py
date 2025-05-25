from pydantic import BaseModel
from typing import List


class AnalyzeFileRequest(BaseModel):
    file_id: str


class AnalyzeFileResponse(BaseModel):
    file_id: str
    existing: bool
    word_count: int
    paragraph_count: int
    top_chars: List[str]
