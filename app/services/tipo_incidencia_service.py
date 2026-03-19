from sqlalchemy.orm import Session
from uuid import UUID
from typing import List, Optional, Tuple

from app.repositories.tipo_incidencia_repository import TipoIncidenciaRepository
from app.schemas.tipo_incidencia_schema import TipoIncidenciaCreate, TipoIncidenciaUpdate
from app.models.tipo_incidencia import TipoIncidencia, EstadoTipoEnum, PrioridadEnum
from app.core.errors import NotFoundException, BusinessRuleException, ConflictException

class TipoIncidenciaService:
    def __init__(self, db: Session):
        self.repository = TipoIncidenciaRepository(db)
        self.db = db

    def create(self, data: TipoIncidenciaCreate) -> TipoIncidencia:
        obj = self.repository.create(data)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def get_by_id(self, id: UUID) -> TipoIncidencia:
        obj = self.repository.get_by_id(id)
        if not obj:
            raise NotFoundException(mensaje="Tipo de incidencia no encontrado", detalle=f"ID: {id}")
        return obj

    def get_all(self, skip: int = 0, limit: int = 10, estado: Optional[EstadoTipoEnum] = None, prioridad: Optional[PrioridadEnum] = None, requiere_servicio_externo: Optional[bool] = None) -> Tuple[List[TipoIncidencia], int]:
        return self.repository.get_all(skip, limit, estado, prioridad, requiere_servicio_externo)

    def update(self, id: UUID, data: TipoIncidenciaUpdate) -> TipoIncidencia:
        obj = self.get_by_id(id)
        updated_obj = self.repository.update(obj, data)
        self.db.commit()
        self.db.refresh(updated_obj)
        return updated_obj

    def activate_deactivate(self, id: UUID, nuevo_estado: EstadoTipoEnum) -> TipoIncidencia:
        obj = self.get_by_id(id)
        if obj.estado == nuevo_estado:
            raise ConflictException(mensaje="El tipo de incidencia ya se encuentra en ese estado")
        updated_obj = self.repository.activate_deactivate(obj, nuevo_estado)
        self.db.commit()
        self.db.refresh(updated_obj)
        return updated_obj

    def delete(self, id: UUID) -> TipoIncidencia:
        obj = self.get_by_id(id)
        if obj.reclamos and len(obj.reclamos) > 0:
            raise BusinessRuleException(mensaje="No se puede eliminar un tipo de incidencia que tiene reclamos asociados")
        deleted_obj = self.repository.soft_delete(obj)
        self.db.commit()
        return deleted_obj
