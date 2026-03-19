from sqlalchemy import Column, String, Text, Boolean, Integer, DateTime, Enum, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
import enum
from app.database import Base

class PrioridadEnum(str, enum.Enum):
    baja = "baja"
    media = "media"
    alta = "alta"
    critica = "critica"

class EstadoTipoEnum(str, enum.Enum):
    activo = "activo"
    inactivo = "inactivo"

class TipoIncidencia(Base):
    __tablename__ = "tipos_incidencia"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    codigo = Column(String(50), unique=True, index=True, nullable=False)
    nombre = Column(String(200), nullable=False)
    descripcion = Column(Text, nullable=True)
    prioridad = Column(Enum(PrioridadEnum), nullable=False)
    tiempo_resolucion_horas = Column(Integer, nullable=False)
    requiere_servicio_externo = Column(Boolean, default=False, nullable=False)
    estado = Column(Enum(EstadoTipoEnum), default=EstadoTipoEnum.activo, nullable=False)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True), nullable=True)
    
    reclamos = relationship("Reclamo", back_populates="tipo_incidencia")
