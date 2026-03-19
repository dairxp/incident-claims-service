from sqlalchemy import Column, String, Text, DateTime, Enum, ForeignKey, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
import enum
from app.database import Base
from app.models.tipo_incidencia import PrioridadEnum

class EstadoReclamoEnum(str, enum.Enum):
    abierto = "abierto"
    en_proceso = "en_proceso"
    resuelto = "resuelto"
    cerrado = "cerrado"
    rechazado = "rechazado"

class Reclamo(Base):
    __tablename__ = "reclamos"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    codigo = Column(String(50), unique=True, index=True, nullable=False)
    titulo = Column(String(200), nullable=False)
    descripcion = Column(Text, nullable=False)
    
    tipo_incidencia_id = Column(UUID(as_uuid=True), ForeignKey("tipos_incidencia.id"), nullable=False)
    tipo_incidencia = relationship("TipoIncidencia", back_populates="reclamos")
    
    estado = Column(Enum(EstadoReclamoEnum), default=EstadoReclamoEnum.abierto, nullable=False)
    prioridad = Column(Enum(PrioridadEnum), nullable=False)
    
    nombre_reportante = Column(String(200), nullable=False)
    contacto_reportante = Column(String(200), nullable=False)
    ubicacion = Column(String(200), nullable=False)
    asignado_a = Column(String(200), nullable=True)
    motivo_rechazo = Column(Text, nullable=True)
    
    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())
    fecha_actualizacion = Column(DateTime(timezone=True), onupdate=func.now())
    fecha_cierre = Column(DateTime(timezone=True), nullable=True)
    deleted_at = Column(DateTime(timezone=True), nullable=True)
    
    historial_estados = relationship("HistorialEstado", back_populates="reclamo", cascade="all, delete-orphan")
