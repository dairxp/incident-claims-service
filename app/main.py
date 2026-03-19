from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import api_router
from app.core.config import settings
from app.core.errors import BaseCustomException, custom_exception_handler
from app.core.logger import logger

app = FastAPI(
    title="Microservicio de Reclamos e Incidencias",
    description="API para la gestión de reclamos e incidencias del sector administrativo",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_exception_handler(BaseCustomException, custom_exception_handler)

app.include_router(api_router)

@app.get("/health", response_model=dict, tags=["Health"])
def health_check():
    logger.info("Health check endpoint called")
    return {"status": "ok", "env": settings.APP_ENV}
