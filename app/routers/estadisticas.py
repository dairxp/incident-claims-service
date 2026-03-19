from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional
from uuid import UUID
from datetime import datetime

from app.database import get_db
from app.services.reclamo_service import ReclamoService
from app.schemas.reclamo_schema import ReclamoResponse
from app.models.reclamo import EstadoReclamoEnum

router = APIRouter()

def get_service(db: Session = Depends(get_db)) -> ReclamoService:
    return ReclamoService(db)

@router.get("/resumen", response_model=dict)
def get_estadisticas_resumen(service: ReclamoService = Depends(get_service)):
    resumen = service.get_estadisticas_resumen()
    return {"success": True, "data": resumen, "mensaje": "Resumen de estadísticas obtenido exitosamente"}

@router.get("/reclamos", response_model=dict)
def get_estadisticas_reclamos(
    fecha_desde: Optional[datetime] = None,
    fecha_hasta: Optional[datetime] = None,
    estado: Optional[EstadoReclamoEnum] = None,
    tipo_incidencia_id: Optional[UUID] = None,
    service: ReclamoService = Depends(get_service)
):
    items = service.get_estadisticas_reclamos(fecha_desde, fecha_hasta, estado, tipo_incidencia_id)
    return {
        "success": True,
        "data": [ReclamoResponse.model_validate(item).model_dump(mode='json') for item in items],
        "mensaje": "Lista completa de reclamos obtenida exitosamente para el reporte"
    }
