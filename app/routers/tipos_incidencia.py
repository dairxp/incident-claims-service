from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from typing import Optional
from uuid import UUID

from app.database import get_db
from app.services.tipo_incidencia_service import TipoIncidenciaService
from app.schemas.tipo_incidencia_schema import (
    TipoIncidenciaCreate, 
    TipoIncidenciaUpdate, 
    TipoIncidenciaResponse
)
from app.models.tipo_incidencia import EstadoTipoEnum, PrioridadEnum

router = APIRouter()

def get_service(db: Session = Depends(get_db)) -> TipoIncidenciaService:
    return TipoIncidenciaService(db)

@router.post("", response_model=dict, status_code=status.HTTP_201_CREATED)
def create_tipo_incidencia(data: TipoIncidenciaCreate, service: TipoIncidenciaService = Depends(get_service)):
    obj = service.create(data)
    return {"success": True, "data": TipoIncidenciaResponse.model_validate(obj).model_dump(mode='json'), "mensaje": "Tipo de incidencia creado exitosamente"}

@router.get("", response_model=dict)
def get_tipos_incidencia(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    estado: Optional[EstadoTipoEnum] = None,
    prioridad: Optional[PrioridadEnum] = None,
    requiere_servicio_externo: Optional[bool] = None,
    service: TipoIncidenciaService = Depends(get_service)
):
    skip = (page - 1) * limit
    items, total = service.get_all(skip, limit, estado, prioridad, requiere_servicio_externo)
    return {
        "success": True,
        "data": {
            "items": [TipoIncidenciaResponse.model_validate(item).model_dump(mode='json') for item in items],
            "total": total,
            "page": page,
            "limit": limit
        },
        "mensaje": "Lista de tipos de incidencia obtenida exitosamente"
    }

@router.get("/{id}", response_model=dict)
def get_tipo_incidencia(id: UUID, service: TipoIncidenciaService = Depends(get_service)):
    obj = service.get_by_id(id)
    return {"success": True, "data": TipoIncidenciaResponse.model_validate(obj).model_dump(mode='json'), "mensaje": "Tipo de incidencia obtenido exitosamente"}

@router.put("/{id}", response_model=dict)
def update_tipo_incidencia(id: UUID, data: TipoIncidenciaUpdate, service: TipoIncidenciaService = Depends(get_service)):
    obj = service.update(id, data)
    return {"success": True, "data": TipoIncidenciaResponse.model_validate(obj).model_dump(mode='json'), "mensaje": "Tipo de incidencia actualizado exitosamente"}

@router.patch("/{id}/estado", response_model=dict)
def activate_deactivate_tipo_incidencia(id: UUID, estado: EstadoTipoEnum = Query(...), service: TipoIncidenciaService = Depends(get_service)):
    obj = service.activate_deactivate(id, estado)
    return {"success": True, "data": TipoIncidenciaResponse.model_validate(obj).model_dump(mode='json'), "mensaje": f"Tipo de incidencia cambiado a {estado.value} exitosamente"}

@router.delete("/{id}", response_model=dict)
def delete_tipo_incidencia(id: UUID, service: TipoIncidenciaService = Depends(get_service)):
    obj = service.delete(id)
    return {"success": True, "data": {"id": str(obj.id)}, "mensaje": "Tipo de incidencia eliminado exitosamente"}
