from sqlalchemy import Column, String, Text, DateTime, ForeignKey, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from app.database import Base

class HistorialEstado(Base):
    __tablename__ = "historial_estados"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    reclamo_id = Column(UUID(as_uuid=True), ForeignKey("reclamos.id"), nullable=False)
    
    estado_anterior = Column(String(50), nullable=False)
    estado_nuevo = Column(String(50), nullable=False)
    comentario = Column(Text, nullable=True)
    cambiado_por = Column(String(200), nullable=False)
    fecha = Column(DateTime(timezone=True), server_default=func.now())
    
    reclamo = relationship("Reclamo", back_populates="historial_estados")
