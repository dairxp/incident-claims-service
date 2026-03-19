from fastapi import APIRouter
from app.routers import tipos_incidencia, reclamos, estadisticas

api_router = APIRouter()

api_router.include_router(tipos_incidencia.router, prefix="/api/v1/tipos-incidencia", tags=["Tipos de Incidencia"])
api_router.include_router(reclamos.router, prefix="/api/v1/reclamos", tags=["Reclamos"])
api_router.include_router(estadisticas.router, prefix="/api/v1/estadisticas", tags=["Estadísticas"])
