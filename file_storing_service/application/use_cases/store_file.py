import hashlib
import uuid
from file_storing_service.application.dtos import StoreFileRequest, StoreFileResponse
from file_storing_service.domain.repositories import FileRepository
from file_storing_service.domain.entities import FileEntity
from file_storing_service.application.ports.storage_port import StorageGateway


class StoreFile:
    def __init__(self, repo: FileRepository, storage: StorageGateway):
        self.repo = repo
        self.storage = storage

    def execute(self, req: StoreFileRequest) -> StoreFileResponse:
        file_hash = hashlib.sha256(req.content).hexdigest()
        existing = self.repo.find_by_hash(file_hash)
        if existing:
            return StoreFileResponse(file_id=existing.id, existing=True)

        new_id = str(uuid.uuid4())
        location = self.storage.save(new_id, req.content)
        entity = FileEntity(id=new_id, name=req.name, hash=file_hash, location=location)
        self.repo.add(entity)
        return StoreFileResponse(file_id=new_id)
