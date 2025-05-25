from sqlalchemy import Column, String, Integer, Text, DateTime, JSON
from file_analysis_service.infrastructure.db.database import Base
from datetime import datetime


class AnalysisResultModel(Base):
    __tablename__ = "analysis_results"

    file_id = Column(String, primary_key=True, index=True)
    word_count = Column(Integer, nullable=False)
    paragraph_count = Column(Integer, nullable=False)
    top_chars = Column(JSON, nullable=False)  # список из 10 символов
    image_location = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
