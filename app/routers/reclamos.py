from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from typing import Optional
from uuid import UUID
from datetime import datetime

from app.database import get_db
from app.services.reclamo_service import ReclamoService
from app.schemas.reclamo_schema import (
    ReclamoCreate,
    ReclamoUpdate,
    ReclamoEstadoUpdate,
    ReclamoResponse,
    ReclamoDetailResponse
)
from app.models.reclamo import EstadoReclamoEnum
from app.models.tipo_incidencia import PrioridadEnum

router = APIRouter()

def get_service(db: Session = Depends(get_db)) -> ReclamoService:
    return ReclamoService(db)

@router.post("", response_model=dict, status_code=status.HTTP_201_CREATED)
def create_reclamo(data: ReclamoCreate, service: ReclamoService = Depends(get_service)):
    obj = service.create(data)
    return {"success": True, "data": ReclamoResponse.model_validate(obj).model_dump(mode='json'), "mensaje": "Reclamo creado exitosamente"}

@router.get("", response_model=dict)
def get_reclamos(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    estado: Optional[EstadoReclamoEnum] = None,
    tipo_incidencia_id: Optional[UUID] = None,
    prioridad: Optional[PrioridadEnum] = None,
    fecha_desde: Optional[datetime] = None,
    fecha_hasta: Optional[datetime] = None,
    service: ReclamoService = Depends(get_service)
):
    skip = (page - 1) * limit
    items, total = service.get_all(skip, limit, estado, tipo_incidencia_id, prioridad, fecha_desde, fecha_hasta)
    return {
        "success": True,
        "data": {
            "items": [ReclamoResponse.model_validate(item).model_dump(mode='json') for item in items],
            "total": total,
            "page": page,
            "limit": limit
        },
        "mensaje": "Lista de reclamos obtenida exitosamente"
    }

@router.get("/{id}", response_model=dict)
def get_reclamo(id: UUID, service: ReclamoService = Depends(get_service)):
    obj = service.get_by_id(id)
    return {"success": True, "data": ReclamoDetailResponse.model_validate(obj).model_dump(mode='json'), "mensaje": "Reclamo obtenido exitosamente"}

@router.put("/{id}", response_model=dict)
def update_reclamo(id: UUID, data: ReclamoUpdate, service: ReclamoService = Depends(get_service)):
    obj = service.update(id, data)
    return {"success": True, "data": ReclamoResponse.model_validate(obj).model_dump(mode='json'), "mensaje": "Reclamo actualizado exitosamente"}

@router.patch("/{id}/estado", response_model=dict)
def change_reclamo_estado(id: UUID, data: ReclamoEstadoUpdate, service: ReclamoService = Depends(get_service)):
    obj = service.change_state(id, data)
    return {"success": True, "data": ReclamoDetailResponse.model_validate(obj).model_dump(mode='json'), "mensaje": "Estado de reclamo actualizado exitosamente"}

@router.delete("/{id}", response_model=dict)
def delete_reclamo(id: UUID, service: ReclamoService = Depends(get_service)):
    obj = service.delete(id)
    return {"success": True, "data": {"id": str(obj.id)}, "mensaje": "Reclamo eliminado exitosamente"}
