from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List
from datetime import datetime
from uuid import UUID
from app.models.reclamo import EstadoReclamoEnum
from app.models.tipo_incidencia import PrioridadEnum

# Historial Schema
class HistorialEstadoResponse(BaseModel):
    id: UUID
    estado_anterior: str
    estado_nuevo: str
    comentario: Optional[str]
    cambiado_por: str
    fecha: datetime
    
    model_config = ConfigDict(from_attributes=True)

class ReclamoBase(BaseModel):
    titulo: str = Field(..., max_length=200)
    descripcion: str
    tipo_incidencia_id: UUID
    nombre_reportante: str = Field(..., max_length=200)
    contacto_reportante: str = Field(..., max_length=200)
    ubicacion: str = Field(..., max_length=200)

class ReclamoCreate(ReclamoBase):
    pass

class ReclamoUpdate(BaseModel):
    titulo: Optional[str] = Field(None, max_length=200)
    descripcion: Optional[str] = None
    tipo_incidencia_id: Optional[UUID] = None
    nombre_reportante: Optional[str] = Field(None, max_length=200)
    contacto_reportante: Optional[str] = Field(None, max_length=200)
    ubicacion: Optional[str] = Field(None, max_length=200)
    asignado_a: Optional[str] = Field(None, max_length=200)

class ReclamoEstadoUpdate(BaseModel):
    estado: EstadoReclamoEnum
    comentario: Optional[str] = None
    motivo_rechazo: Optional[str] = None
    cambiado_por: str = Field(..., max_length=200)

class ReclamoResponse(ReclamoBase):
    id: UUID
    codigo: str
    estado: EstadoReclamoEnum
    prioridad: PrioridadEnum
    asignado_a: Optional[str] = None
    motivo_rechazo: Optional[str] = None
    fecha_creacion: datetime
    fecha_actualizacion: Optional[datetime]
    fecha_cierre: Optional[datetime]
    
    model_config = ConfigDict(from_attributes=True)

class ReclamoDetailResponse(ReclamoResponse):
    historial_estados: List[HistorialEstadoResponse] = []
