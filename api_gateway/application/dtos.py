from pydantic import BaseModel
from typing import Dict, Any


class ProxyRequestDTO(BaseModel):
    method: str
    path: str
    headers: Dict[str, Any]
    content: bytes


class ProxyResponseDTO(BaseModel):
    status_code: int
    headers: Dict[str, Any]
    content: bytes
