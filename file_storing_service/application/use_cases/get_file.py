from fastapi import HTTPException
from file_storing_service.application.dtos import GetFileResponse
from file_storing_service.domain.repositories import FileRepository
from file_storing_service.application.ports.storage_port import StorageGateway


class GetFile:
    def __init__(self, repo: FileRepository, storage: StorageGateway):
        self.repo = repo
        self.storage = storage

    def execute(self, file_id: str) -> GetFileResponse:
        entity = self.repo.find_by_id(file_id)
        if not entity:
            raise HTTPException(status_code=404, detail="File not found")
        content = self.storage.load(entity.location)
        return GetFileResponse(name=entity.name, content=content)
