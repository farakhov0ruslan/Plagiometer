import os
from fastapi import FastAPI
from file_storing_service.presentation.controllers.file_controller import router as file_router

os.makedirs("data", exist_ok=True)

app = FastAPI(
    title="File Storing Service",
    version="1.0",
    description="Сервис для загрузки и скачивания файлов"
)

# Подключаем роуты из presentation слоя
# В контроллере они уже объявлены на /files/…
app.include_router(file_router, prefix="")


@app.get("/health", tags=["health"])
def health():
    return {"status": "alive"}
