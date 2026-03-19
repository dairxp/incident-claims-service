from sqlalchemy.orm import Session
from sqlalchemy import select, func
from typing import List, Optional, Tuple
from uuid import UUID
from datetime import datetime, timezone

from app.models.tipo_incidencia import TipoIncidencia, EstadoTipoEnum, PrioridadEnum
from app.schemas.tipo_incidencia_schema import TipoIncidenciaCreate, TipoIncidenciaUpdate

class TipoIncidenciaRepository:
    def __init__(self, session: Session):
        self.session = session

    def _generate_codigo(self) -> str:
        stmt = select(TipoIncidencia.codigo).order_by(TipoIncidencia.codigo.desc()).limit(1)
        last_code = self.session.execute(stmt).scalar_one_or_none()
        if not last_code:
            return "INC001"
        try:
            num = int(last_code[3:])
            return f"INC{num + 1:03d}"
        except ValueError:
            return "INC001"

    def create(self, data: TipoIncidenciaCreate) -> TipoIncidencia:
        db_obj = TipoIncidencia(
            codigo=self._generate_codigo(),
            **data.model_dump()
        )
        self.session.add(db_obj)
        self.session.flush()
        return db_obj

    def get_by_id(self, id: UUID) -> Optional[TipoIncidencia]:
        stmt = select(TipoIncidencia).where(TipoIncidencia.id == id, TipoIncidencia.fecha_eliminacion.is_(None))
        return self.session.execute(stmt).scalar_one_or_none()
    
    def get_all(self, skip: int = 0, limit: int = 10, estado: Optional[EstadoTipoEnum] = None, prioridad: Optional[PrioridadEnum] = None, requiere_servicio_externo: Optional[bool] = None) -> Tuple[List[TipoIncidencia], int]:
        stmt = select(TipoIncidencia).where(TipoIncidencia.fecha_eliminacion.is_(None))
        
        if estado:
            stmt = stmt.where(TipoIncidencia.estado == estado)
        if prioridad:
            stmt = stmt.where(TipoIncidencia.prioridad == prioridad)
        if requiere_servicio_externo is not None:
            stmt = stmt.where(TipoIncidencia.requiere_servicio_externo == requiere_servicio_externo)
            
        count_stmt = select(func.count()).select_from(stmt.subquery())
        total = self.session.execute(count_stmt).scalar() or 0
        
        stmt = stmt.offset(skip).limit(limit).order_by(TipoIncidencia.fecha_creacion.desc())
        items = self.session.execute(stmt).scalars().all()
        
        return list(items), total

    def update(self, db_obj: TipoIncidencia, data: TipoIncidenciaUpdate) -> TipoIncidencia:
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(db_obj, field, value)
        self.session.flush()
        return db_obj

    def soft_delete(self, db_obj: TipoIncidencia) -> TipoIncidencia:
        db_obj.fecha_eliminacion = datetime.now(timezone.utc)
        self.session.flush()
        return db_obj

    def activate_deactivate(self, db_obj: TipoIncidencia, nuevo_estado: EstadoTipoEnum) -> TipoIncidencia:
        db_obj.estado = nuevo_estado
        self.session.flush()
        return db_obj
