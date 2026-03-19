# Microservicio de Reclamos e Incidencias

API REST para la gestion de reclamos e incidencias del sector administrativo universitario. Construida con FastAPI + PostgreSQL + SQLAlchemy.

[![lang en](https://img.shields.io/badge/lang-en-8a8a8a?style=for-the-badge)](README.en.md)
[![lang es](https://img.shields.io/badge/lang-es-c9a227?style=for-the-badge)](README.md)

---

## Stack tecnologico

| Tecnologia | Version |
|---|---|
| Python | 3.11+ |
| FastAPI | 0.115.5 |
| SQLAlchemy | 2.0.36 |
| PostgreSQL | 16 |
| Pydantic | 2.10.3 |
| Alembic | 1.14.0 |

---

## Levantar el proyecto con Docker

### 1. Clonar y entrar a la carpeta

```bash
cd incident-claims-service
```

### 2. Crear el archivo `.env`

```bash
cp .env.example .env
```

### 3. Levantar los servicios

```bash
docker-compose up --build
```

La API estara disponible en: http://localhost:8000  
Documentacion Swagger: http://localhost:8000/docs

---

## Ejecutar migraciones (primera vez)

Dentro del contenedor `api`:

```bash
docker-compose exec api alembic upgrade head
```

O desde tu entorno local (con la BD accesible):

```bash
alembic upgrade head
```

---

## Ejecutar tests

```bash
# Instalar dependencias
pip install -r requirements.txt

# Ejecutar tests
pytest tests/ -v
```

---

## Endpoints disponibles

### Health Check

| Metodo | Ruta | Descripcion |
|---|---|---|
| GET | `/health` | Estado del servicio |

### Tipos de Incidencia

| Metodo | Ruta | Descripcion |
|---|---|---|
| POST | `/api/v1/tipos-incidencia` | Crear tipo |
| GET | `/api/v1/tipos-incidencia` | Listar con filtros y paginacion |
| GET | `/api/v1/tipos-incidencia/{id}` | Ver detalle |
| PUT | `/api/v1/tipos-incidencia/{id}` | Actualizar |
| PATCH | `/api/v1/tipos-incidencia/{id}/estado` | Activar/Desactivar |
| DELETE | `/api/v1/tipos-incidencia/{id}` | Soft delete |

### Reclamos

| Metodo | Ruta | Descripcion |
|---|---|---|
| POST | `/api/v1/reclamos` | Crear reclamo |
| GET | `/api/v1/reclamos` | Listar con filtros y paginacion |
| GET | `/api/v1/reclamos/{id}` | Detalle + historial |
| PATCH | `/api/v1/reclamos/{id}/estado` | Cambiar estado |
| PUT | `/api/v1/reclamos/{id}` | Editar reclamo |
| DELETE | `/api/v1/reclamos/{id}` | Soft delete |

### Estadisticas (para microservicio de reportes)

| Metodo | Ruta | Descripcion |
|---|---|---|
| GET | `/api/v1/estadisticas/resumen` | Totales por estado/prioridad/tipo |
| GET | `/api/v1/estadisticas/reclamos` | Lista completa sin paginacion |

---

## Transiciones de estado de reclamos

```text
abierto -> en_proceso
en_proceso -> resuelto
en_proceso -> rechazado  (requiere motivo_rechazo)
resuelto -> cerrado
```

---

## Estructura del proyecto

```text
incident-claims-service/
|- app/
|  |- __init__.py
|  |- main.py
|  |- database.py
|  |- core/
|  |  |- __init__.py
|  |  |- config.py
|  |  |- errors.py
|  |  |- logger.py
|  |- models/
|  |  |- __init__.py
|  |  |- historial_estado.py
|  |  |- reclamo.py
|  |  |- tipo_incidencia.py
|  |- repositories/
|  |  |- __init__.py
|  |  |- reclamo_repository.py
|  |  |- tipo_incidencia_repository.py
|  |- routers/
|  |  |- __init__.py
|  |  |- estadisticas.py
|  |  |- reclamos.py
|  |  |- tipos_incidencia.py
|  |- schemas/
|  |  |- __init__.py
|  |  |- reclamo_schema.py
|  |  |- tipo_incidencia_schema.py
|  |- services/
|     |- __init__.py
|     |- reclamo_service.py
|     |- tipo_incidencia_service.py
|- alembic/
|  |- env.py
|  |- script.py.mako
|  |- versions/
|     |- 001_initial.py
|- tests/
|  |- test_reclamos.py
|  |- test_tipos_incidencia.py
|- requirements.txt
|- Dockerfile
|- docker-compose.yml
|- alembic.ini
|- README.md
|- README.en.md
```

---

## Notas adicionales

- Recuerda crear y configurar el archivo `.env` antes de levantar los servicios.
- Los archivos y carpetas como `__pycache__/`, `.env`, `venv/`, y temporales deben ignorarse en Git.
- Las migraciones de Alembic estan en `alembic/versions/`.
- Los tests unitarios estan en `tests/`.

---

## Licencia

Elaborado por DairXP
