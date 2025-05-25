from fastapi import FastAPI
from routers.files import router as files_router
from routers.analysis import router as analysis_router

app = FastAPI(
    title="API Gateway",
    version="1.0",
    description="Прокси для File Storing и File Analysis"
)


@app.get("/health", tags=["health"])
def health():
    return {"status": "alive"}


# файлы
app.include_router(files_router)

# анализ
app.include_router(analysis_router)
