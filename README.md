

# Incident Claims Service / Microservicio de Reclamos e Incidencias

<details>
<summary><strong>🌐 English (default)</strong> — <em>Click for Español</em></summary>

## Incident Claims Service

REST API for managing claims and incidents in the university administrative sector. Built with **FastAPI + PostgreSQL + SQLAlchemy**.

---

## Tech Stack

| Technology | Version |
|---|---|
| Python | 3.11+ |
| FastAPI | 0.115.5 |
| SQLAlchemy | 2.0.36 |
| PostgreSQL | 16 |
| Pydantic | 2.10.3 |
| Alembic | 1.14.0 |

---

## Run the project with Docker

### 1. Clone and enter the folder

```bash
cd incident-claims-service
```

### 2. Create the `.env` file

```bash
cp .env.example .env
```

### 3. Start the services

```bash
docker-compose up --build
```

The API will be available at: **http://localhost:8000**  
Swagger docs: **http://localhost:8000/docs**

---

## Run migrations (first time)

Inside the `api` container:

```bash
docker-compose exec api alembic upgrade head
```

Or from your local environment (with DB accessible):

```bash
alembic upgrade head
```

---

## Run tests

```bash
# Install dependencies
pip install -r requirements.txt

# Run tests
pytest tests/ -v
```

---

## Available Endpoints

### Health Check
| Method | Path | Description |
|---|---|---|
| GET | `/health` | Service status |

### Incident Types
| Method | Path | Description |
|---|---|---|
| POST | `/api/v1/tipos-incidencia` | Create type |
| GET | `/api/v1/tipos-incidencia` | List with filters and pagination |
| GET | `/api/v1/tipos-incidencia/{id}` | Get details |
| PUT | `/api/v1/tipos-incidencia/{id}` | Update |
| PATCH | `/api/v1/tipos-incidencia/{id}/estado` | Activate/Deactivate |
| DELETE | `/api/v1/tipos-incidencia/{id}` | Soft delete |

### Claims
| Method | Path | Description |
|---|---|---|
| POST | `/api/v1/reclamos` | Create claim |
| GET | `/api/v1/reclamos` | List with filters and pagination |
| GET | `/api/v1/reclamos/{id}` | Details + history |
| PATCH | `/api/v1/reclamos/{id}/estado` | Change status |
| PUT | `/api/v1/reclamos/{id}` | Edit claim |
| DELETE | `/api/v1/reclamos/{id}` | Soft delete |

### Statistics (for reporting microservice)
| Method | Path | Description |
|---|---|---|
| GET | `/api/v1/estadisticas/resumen` | Totals by status/priority/type |
| GET | `/api/v1/estadisticas/reclamos` | Full list without pagination |

---

## Claim status transitions

```
abierto → en_proceso
en_proceso → resuelto
en_proceso → rechazado  (requires motivo_rechazo)
resuelto → cerrado
```

---

## Project structure

```
incident-claims-service/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── database.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py
│   │   ├── errors.py
│   │   └── logger.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── historial_estado.py
│   │   ├── reclamo.py
│   │   └── tipo_incidencia.py
│   ├── repositories/
│   │   ├── __init__.py
│   │   ├── reclamo_repository.py
│   │   └── tipo_incidencia_repository.py
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── estadisticas.py
│   │   ├── reclamos.py
│   │   └── tipos_incidencia.py
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── reclamo_schema.py
│   │   └── tipo_incidencia_schema.py
│   └── services/
│       ├── __init__.py
│       ├── reclamo_service.py
│       └── tipo_incidencia_service.py
├── alembic/
│   ├── env.py
│   ├── script.py.mako
│   └── versions/
│       └── 001_initial.py
├── tests/
│   ├── test_reclamos.py
│   └── test_tipos_incidencia.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── alembic.ini
└── README.md
```

---

## Additional notes

- Remember to create and configure the `.env` file before starting the services.
- Ignore files and folders like `__pycache__/`, `.env`, `venv/`, and temporary files in version control.
- Alembic migrations are in `alembic/versions/`.
- Unit tests are in the `tests/` folder.

---

## License

Created by DairXP

</details>

<details open>
<summary><strong>🇪🇸 Español</strong> — <em>Haz clic para English</em></summary>

# Microservicio de Reclamos e Incidencias

API REST para la gestión de reclamos e incidencias del sector administrativo universitario. Construida con **FastAPI + PostgreSQL + SQLAlchemy**.

---

## Stack tecnológico

| Tecnología | Versión |
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

La API estará disponible en: **http://localhost:8000**
Documentación Swagger: **http://localhost:8000/docs**

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
| Método | Ruta | Descripción |
|---|---|---|
| GET | `/health` | Estado del servicio |

### Tipos de Incidencia
| Método | Ruta | Descripción |
|---|---|---|
| POST | `/api/v1/tipos-incidencia` | Crear tipo |
| GET | `/api/v1/tipos-incidencia` | Listar con filtros y paginación |
| GET | `/api/v1/tipos-incidencia/{id}` | Ver detalle |
| PUT | `/api/v1/tipos-incidencia/{id}` | Actualizar |
| PATCH | `/api/v1/tipos-incidencia/{id}/estado` | Activar/Desactivar |
| DELETE | `/api/v1/tipos-incidencia/{id}` | Soft delete |

### Reclamos
| Método | Ruta | Descripción |
|---|---|---|
| POST | `/api/v1/reclamos` | Crear reclamo |
| GET | `/api/v1/reclamos` | Listar con filtros y paginación |
| GET | `/api/v1/reclamos/{id}` | Detalle + historial |
| PATCH | `/api/v1/reclamos/{id}/estado` | Cambiar estado |
| PUT | `/api/v1/reclamos/{id}` | Editar reclamo |
| DELETE | `/api/v1/reclamos/{id}` | Soft delete |

### Estadísticas (para microservicio de reportes)
| Método | Ruta | Descripción |
|---|---|---|
| GET | `/api/v1/estadisticas/resumen` | Totales por estado/prioridad/tipo |
| GET | `/api/v1/estadisticas/reclamos` | Lista completa sin paginación |

---

## Transiciones de estado de reclamos

```
abierto → en_proceso
en_proceso → resuelto
en_proceso → rechazado  (requiere motivo_rechazo)
resuelto → cerrado
```

---

## Estructura del proyecto

```
incident-claims-service/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── database.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py
│   │   ├── errors.py
│   │   └── logger.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── historial_estado.py
│   │   ├── reclamo.py
│   │   └── tipo_incidencia.py
│   ├── repositories/
│   │   ├── __init__.py
│   │   ├── reclamo_repository.py
│   │   └── tipo_incidencia_repository.py
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── estadisticas.py
│   │   ├── reclamos.py
│   │   └── tipos_incidencia.py
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── reclamo_schema.py
│   │   └── tipo_incidencia_schema.py
│   └── services/
│       ├── __init__.py
│       ├── reclamo_service.py
│       └── tipo_incidencia_service.py
├── alembic/
│   ├── env.py
│   ├── script.py.mako
│   └── versions/
│       └── 001_initial.py
├── tests/
│   ├── test_reclamos.py
│   └── test_tipos_incidencia.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── alembic.ini
└── README.md
```

---

## Notas adicionales

- Recuerda crear y configurar el archivo `.env` antes de levantar los servicios.
- Los archivos y carpetas como `__pycache__/`, `.env`, `venv/`, y archivos temporales deben ser ignorados en el control de versiones.
- Las migraciones de Alembic se encuentran en `alembic/versions/`.
- Los tests unitarios están en la carpeta `tests/`.

---

## Licencia

Elaborado por DairXP

</details>
