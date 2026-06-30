from fastapi import FastAPI
from api.routes.health import router as health_router
from api.routes.sessions import router as sessions_router
from api.routes.files import router as files_router

def create_app() -> FastAPI:
    app = FastAPI(title="Ecommerce Agent Platform V3", version="0.3.0")
    app.include_router(health_router, prefix="/api/v1")
    app.include_router(sessions_router, prefix="/api/v1")
    app.include_router(files_router, prefix="/api/v1")
    return app
