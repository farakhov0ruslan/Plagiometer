from fastapi import FastAPI
from api_gateway.infrastructure.config import settings
from api_gateway.presentation.controllers.proxy_controller import router as proxy_router

app = FastAPI(title="API Gateway")
app.include_router(proxy_router)

@app.get("/health")
def health():
    return {"status": "ok"}
