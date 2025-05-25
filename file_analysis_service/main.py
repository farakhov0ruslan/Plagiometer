from fastapi import FastAPI
from .presentation.controllers.file_controller import router as file_router


app = FastAPI(title="File Storing Service")
app.include_router(file_router, prefix="/api")
