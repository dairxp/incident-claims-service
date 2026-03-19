from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime
from uuid import UUID
from app.models.tipo_incidencia import PrioridadEnum, EstadoTipoEnum

class TipoIncidenciaBase(BaseModel):
    nombre: str = Field(..., max_length=200)
    descripcion: Optional[str] = None
    prioridad: PrioridadEnum
    tiempo_resolucion_horas: int = Field(..., ge=1)
    requiere_servicio_externo: bool = False
    estado: EstadoTipoEnum = EstadoTipoEnum.activo

class TipoIncidenciaCreate(TipoIncidenciaBase):
    pass

class TipoIncidenciaUpdate(TipoIncidenciaBase):
    pass

class TipoIncidenciaResponse(TipoIncidenciaBase):
    id: UUID
    codigo: str
    created_at: datetime
    updated_at: Optional[datetime]
    
    model_config = ConfigDict(from_attributes=True)
