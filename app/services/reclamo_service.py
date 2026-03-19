from sqlalchemy.orm import Session
from uuid import UUID
from typing import List, Optional, Tuple
from datetime import datetime

from app.repositories.reclamo_repository import ReclamoRepository
from app.repositories.tipo_incidencia_repository import TipoIncidenciaRepository
from app.schemas.reclamo_schema import ReclamoCreate, ReclamoUpdate, ReclamoEstadoUpdate
from app.models.reclamo import Reclamo, EstadoReclamoEnum
from app.models.tipo_incidencia import PrioridadEnum, EstadoTipoEnum
from app.core.errors import NotFoundException, BusinessRuleException, ConflictException

class ReclamoService:
    def __init__(self, db: Session):
        self.repository = ReclamoRepository(db)
        self.tipo_incidencia_repo = TipoIncidenciaRepository(db)
        self.db = db

    def create(self, data: ReclamoCreate) -> Reclamo:
        tipo_incidencia = self.tipo_incidencia_repo.get_by_id(data.tipo_incidencia_id)
        if not tipo_incidencia:
            raise NotFoundException(mensaje="El tipo de incidencia especificado no existe o está eliminado")
        if tipo_incidencia.estado != EstadoTipoEnum.activo:
            raise BusinessRuleException(mensaje="El tipo de incidencia seleccionado no está activo")
            
        reclamo = self.repository.create(data, tipo_incidencia)
        
        # Registrar historial inicial
        self.repository.register_historial(
            reclamo_id=reclamo.id,
            estado_anterior="creación",
            estado_nuevo=reclamo.estado.value,
            comentario="Reclamo creado",
            cambiado_por=data.nombre_reportante
        )
        self.db.commit()
        self.db.refresh(reclamo)
        return reclamo

    def get_by_id(self, id: UUID) -> Reclamo:
        obj = self.repository.get_by_id(id)
        if not obj:
            raise NotFoundException(mensaje="Reclamo no encontrado", detalle=f"ID: {id}")
        return obj

    def get_all(self, skip: int = 0, limit: int = 10, estado: Optional[EstadoReclamoEnum] = None, tipo_incidencia_id: Optional[UUID] = None, prioridad: Optional[PrioridadEnum] = None, fecha_desde: Optional[datetime] = None, fecha_hasta: Optional[datetime] = None) -> Tuple[List[Reclamo], int]:
        return self.repository.get_all(skip, limit, estado, tipo_incidencia_id, prioridad, fecha_desde, fecha_hasta)

    def update(self, id: UUID, data: ReclamoUpdate) -> Reclamo:
        obj = self.get_by_id(id)
        
        # Validar tipo de incidencia si se está actualizando
        if data.tipo_incidencia_id and data.tipo_incidencia_id != obj.tipo_incidencia_id:
            tipo = self.tipo_incidencia_repo.get_by_id(data.tipo_incidencia_id)
            if not tipo:
                raise NotFoundException(mensaje="El nuevo tipo de incidencia no existe")
            if tipo.estado != EstadoTipoEnum.activo:
                raise BusinessRuleException(mensaje="El nuevo tipo de incidencia no está activo")
                
        updated_obj = self.repository.update(obj, data)
        self.db.commit()
        self.db.refresh(updated_obj)
        return updated_obj

    def get_estadisticas_resumen(self):
        return self.repository.get_estadisticas_resumen()

    def get_estadisticas_reclamos(self, fecha_desde: Optional[datetime] = None, fecha_hasta: Optional[datetime] = None, estado: Optional[EstadoReclamoEnum] = None, tipo_incidencia_id: Optional[UUID] = None):
        items, _ = self.repository.get_all(skip=0, limit=0, estado=estado, tipo_incidencia_id=tipo_incidencia_id, fecha_desde=fecha_desde, fecha_hasta=fecha_hasta)
        return items

    def change_state(self, id: UUID, data: ReclamoEstadoUpdate) -> Reclamo:
        obj = self.get_by_id(id)
        
        # Validar transiciones
        estado_actual = obj.estado
        nuevo_estado = data.estado
        
        if estado_actual == nuevo_estado:
            raise ConflictException(mensaje="El reclamo ya se encuentra en ese estado")
            
        transiciones_validas = {
            EstadoReclamoEnum.abierto: [EstadoReclamoEnum.en_proceso],
            EstadoReclamoEnum.en_proceso: [EstadoReclamoEnum.resuelto, EstadoReclamoEnum.rechazado],
            EstadoReclamoEnum.resuelto: [EstadoReclamoEnum.cerrado],
            EstadoReclamoEnum.cerrado: [],
            EstadoReclamoEnum.rechazado: []
        }
        
        if nuevo_estado not in transiciones_validas.get(estado_actual, []):
            raise BusinessRuleException(mensaje=f"Transición de estado inválida. No se puede pasar de {estado_actual.value} a {nuevo_estado.value}")
            
        if nuevo_estado == EstadoReclamoEnum.rechazado and not data.motivo_rechazo:
            raise BusinessRuleException(mensaje="El motivo de rechazo es obligatorio cuando se rechaza un reclamo")
            
        estado_anterior_str = obj.estado.value
        updated_obj = self.repository.change_state(obj, nuevo_estado, data.motivo_rechazo)
        
        # Registrar historial
        self.repository.register_historial(
            reclamo_id=id,
            estado_anterior=estado_anterior_str,
            estado_nuevo=nuevo_estado.value,
            comentario=data.comentario,
            cambiado_por=data.cambiado_por
        )
        
        self.db.commit()
        self.db.refresh(updated_obj)
        return updated_obj

    def delete(self, id: UUID) -> Reclamo:
        obj = self.get_by_id(id)
        deleted_obj = self.repository.soft_delete(obj)
        self.db.commit()
        return deleted_obj
