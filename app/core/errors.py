from fastapi import Request
from fastapi.responses import JSONResponse
from datetime import datetime, timezone

class BaseCustomException(Exception):
    def __init__(self, error: str, mensaje: str, detalle: str = None):
        self.error = error
        self.mensaje = mensaje
        self.detalle = detalle

class NotFoundException(BaseCustomException):
    def __init__(self, mensaje: str, detalle: str = None):
        super().__init__(error="NOT_FOUND", mensaje=mensaje, detalle=detalle)

class ConflictException(BaseCustomException):
    def __init__(self, mensaje: str, detalle: str = None):
        super().__init__(error="CONFLICT", mensaje=mensaje, detalle=detalle)

class BusinessRuleException(BaseCustomException):
    def __init__(self, mensaje: str, detalle: str = None):
        super().__init__(error="BUSINESS_RULE_ERROR", mensaje=mensaje, detalle=detalle)

class BadRequestException(BaseCustomException):
    def __init__(self, mensaje: str, detalle: str = None):
        super().__init__(error="BAD_REQUEST", mensaje=mensaje, detalle=detalle)

def custom_exception_handler(request: Request, exc: BaseCustomException):
    return JSONResponse(
        status_code=get_status_code(exc.error),
        content={
            "error": exc.error,
            "mensaje": exc.mensaje,
            "detalle": exc.detalle,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
    )

def get_status_code(error_type: str) -> int:
    mapping = {
        "NOT_FOUND": 404,
        "CONFLICT": 409,
        "BUSINESS_RULE_ERROR": 422,
        "BAD_REQUEST": 400
    }
    return mapping.get(error_type, 500)
