from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from file_storing_service.infrastructure.db.models import Base, FileModel
from file_storing_service.domain.repositories import FileRepository
from file_storing_service.domain.entities import FileEntity
from file_storing_service.infrastructure.config import settings

engine = create_engine(settings.DATABASE_URL, echo=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


class FileRepoPostgres(FileRepository):
    def __init__(self):
        Base.metadata.create_all(bind=engine)

    def find_by_hash(self, hash: str):
        with SessionLocal() as db:
            q = db.query(FileModel).filter_by(hash=hash).first()
            if not q:
                return None
            data = {
                "id": q.id,
                "name": q.name,
                "hash": q.hash,
                "location": q.location
            }

            return FileEntity(**data)

    def find_by_id(self, file_id: str):
        with SessionLocal() as db:
            q = db.query(FileModel).get(file_id)
            if not q:
                return None
            data = {
                "id": q.id,
                "name": q.name,
                "hash": q.hash,
                "location": q.location
            }

            return FileEntity(**data)

    def add(self, entity: FileEntity):
        with SessionLocal() as db:
            db.add(FileModel(**entity.__dict__))
            db.commit()
