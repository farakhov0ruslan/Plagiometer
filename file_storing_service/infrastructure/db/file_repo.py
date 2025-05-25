from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from .models import Base, FileModel
from ...domain.repositories import FileRepository
from ...domain.entities import FileEntity
from ..config import settings

engine = create_engine(settings.DATABASE_URL, echo=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


class FileRepoPostgres(FileRepository):
    def __init__(self):
        Base.metadata.create_all(bind=engine)

    def find_by_hash(self, hash: str):
        with SessionLocal() as db:
            q = db.query(FileModel).filter_by(hash=hash).first()
            return FileEntity(**q.__dict__) if q else None

    def find_by_id(self, file_id: str):
        with SessionLocal() as db:
            q = db.query(FileModel).get(file_id)
            return FileEntity(**q.__dict__) if q else None

    def add(self, entity: FileEntity):
        with SessionLocal() as db:
            db.add(FileModel(**entity.__dict__))
            db.commit()
