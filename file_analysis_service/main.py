import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from file_analysis_service.infrastructure.db.database import Base, engine
from file_analysis_service.presentation.controllers.analysis_controller import router

# Создаём папку data под статику
os.makedirs("data", exist_ok=True)

# Схема БД
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="File Analysis Service",
    version="1.0",
    description="Анализ файлов и облако слов"
)

# Статика картинок
app.mount("/images", StaticFiles(directory="data"), name="images")

# Основной роутер
app.include_router(router)
