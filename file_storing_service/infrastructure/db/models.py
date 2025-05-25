from sqlalchemy import Column, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class FileModel(Base):
    __tablename__ = "files"
    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    hash = Column(String, unique=True, index=True)
    location = Column(String, nullable=False)
