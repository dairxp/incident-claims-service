from sqlalchemy.orm import Session
from sqlalchemy import select, func, desc
from typing import List, Optional, Tuple
from uuid import UUID
from datetime import datetime, timezone

from app.models.reclamo import Reclamo, EstadoReclamoEnum
from app.models.tipo_incidencia import PrioridadEnum, TipoIncidencia
from app.models.historial_estado import HistorialEstado
from app.schemas.reclamo_schema import ReclamoCreate, ReclamoUpdate

class ReclamoRepository:
    def __init__(self, session: Session):
        self.session = session

    def _generate_codigo(self) -> str:
        stmt = select(Reclamo.codigo).order_by(Reclamo.codigo.desc()).limit(1)
        last_code = self.session.execute(stmt).scalar_one_or_none()
        if not last_code:
            return "REC001"
        try:
            num = int(last_code[3:])
            return f"REC{num + 1:03d}"
        except ValueError:
            return "REC001"

    def create(self, data: ReclamoCreate, tipo_incidencia: TipoIncidencia) -> Reclamo:
        db_obj = Reclamo(
            codigo=self._generate_codigo(),
            prioridad=tipo_incidencia.prioridad,
            **data.model_dump()
        )
        self.session.add(db_obj)
        self.session.flush()
        return db_obj

    def get_by_id(self, id: UUID) -> Optional[Reclamo]:
        stmt = select(Reclamo).where(Reclamo.id == id, Reclamo.fecha_eliminacion.is_(None))
        return self.session.execute(stmt).scalar_one_or_none()
    
    def get_all(self, skip: int = 0, limit: int = 10, estado: Optional[EstadoReclamoEnum] = None, tipo_incidencia_id: Optional[UUID] = None, prioridad: Optional[PrioridadEnum] = None, fecha_desde: Optional[datetime] = None, fecha_hasta: Optional[datetime] = None) -> Tuple[List[Reclamo], int]:
        stmt = select(Reclamo).where(Reclamo.fecha_eliminacion.is_(None))
        
        if estado:
            stmt = stmt.where(Reclamo.estado == estado)
        if tipo_incidencia_id:
            stmt = stmt.where(Reclamo.tipo_incidencia_id == tipo_incidencia_id)
        if prioridad:
            stmt = stmt.where(Reclamo.prioridad == prioridad)
        if fecha_desde:
            stmt = stmt.where(Reclamo.fecha_creacion >= fecha_desde)
        if fecha_hasta:
            stmt = stmt.where(Reclamo.fecha_creacion <= fecha_hasta)
            
        count_stmt = select(func.count()).select_from(stmt.subquery())
        total = self.session.execute(count_stmt).scalar() or 0
        
        if limit > 0:
            stmt = stmt.offset(skip).limit(limit)
            
        stmt = stmt.order_by(desc(Reclamo.fecha_creacion))
        items = self.session.execute(stmt).scalars().all()
        
        return list(items), total

    def update(self, db_obj: Reclamo, data: ReclamoUpdate) -> Reclamo:
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(db_obj, field, value)
        self.session.flush()
        return db_obj

    def soft_delete(self, db_obj: Reclamo) -> Reclamo:
        db_obj.fecha_eliminacion = datetime.now(timezone.utc)
        self.session.flush()
        return db_obj
    
    def register_historial(self, reclamo_id: UUID, estado_anterior: str, estado_nuevo: str, comentario: Optional[str], cambiado_por: str):
        historial = HistorialEstado(
            reclamo_id=reclamo_id,
            estado_anterior=estado_anterior,
            estado_nuevo=estado_nuevo,
            comentario=comentario,
            cambiado_por=cambiado_por
        )
        self.session.add(historial)
        self.session.flush()

    def change_state(self, db_obj: Reclamo, nuevo_estado: EstadoReclamoEnum, motivo_rechazo: Optional[str] = None):
        db_obj.estado = nuevo_estado
        if nuevo_estado == EstadoReclamoEnum.rechazado and motivo_rechazo:
            db_obj.motivo_rechazo = motivo_rechazo
        if nuevo_estado in (EstadoReclamoEnum.rechazado, EstadoReclamoEnum.cerrado):
            db_obj.fecha_cierre = datetime.now(timezone.utc)
        self.session.flush()
        return db_obj

    def get_estadisticas_resumen(self):
        total = self.session.scalar(select(func.count()).select_from(Reclamo).where(Reclamo.fecha_eliminacion.is_(None))) or 0
        
        estados = self.session.execute(
            select(Reclamo.estado, func.count(Reclamo.id)).where(Reclamo.fecha_eliminacion.is_(None)).group_by(Reclamo.estado)
        ).all()
        
        prioridades = self.session.execute(
            select(Reclamo.prioridad, func.count(Reclamo.id)).where(Reclamo.fecha_eliminacion.is_(None)).group_by(Reclamo.prioridad)
        ).all()
        
        tipos = self.session.execute(
            select(TipoIncidencia.nombre, func.count(Reclamo.id))
            .join(Reclamo.tipo_incidencia)
            .where(Reclamo.fecha_eliminacion.is_(None))
            .group_by(TipoIncidencia.nombre)
        ).all()
        
        return {
            "total_reclamos": total,
            "por_estado": {e.value if hasattr(e, 'value') else e: count for e, count in estados},
            "por_prioridad": {p.value if hasattr(p, 'value') else p: count for p, count in prioridades},
            "por_tipo": {t: count for t, count in tipos}
        }
