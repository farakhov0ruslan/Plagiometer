from pydantic import BaseModel
from typing import List


class UploadResponse(BaseModel):
    file_id: str
    existing: bool = False


class FileInfo(BaseModel):
    id: str
    name: str
    hash: str
    location: str


class AnalyzeFileResponse(BaseModel):
    file_id: str
    existing: bool
    word_count: int
    paragraph_count: int
    top_chars: List[str]
