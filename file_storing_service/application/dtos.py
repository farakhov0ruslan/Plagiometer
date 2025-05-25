from pydantic import BaseModel


class StoreFileRequest(BaseModel):
    name: str
    content: bytes


class StoreFileResponse(BaseModel):
    file_id: str
    existing: bool = False


class GetFileResponse(BaseModel):
    name: str
    content: bytes
