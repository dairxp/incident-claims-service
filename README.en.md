# Complaints and Incidents Microservice

REST API for the management of complaints and incidents in the university administrative sector. Built with FastAPI + PostgreSQL + SQLAlchemy.

[![lang en](https://img.shields.io/badge/lang-en-8a8a8a?style=for-the-badge)](README.en.md)[![lang es](https://img.shields.io/badge/lang-es-c9a227?style=for-the-badge)](README.md)

* * *

## Technology stack

| Technology | Version |
| ---------- | ------- |
| Python     | 3.11+   |
| speedy     | 0.115.5 |
| SQLAlchemy | 2.0.36  |
| PostgreSQL | 16      |
| Pydantic   | 2.10.3  |
| Alembic    | 1.14.0  |

* * *

## Launch the project with Docker

### 1. Clone and enter the folder

```bash
cd incident-claims-service
```

### 2. Create the file`.env`

```bash
cp .env.example .env
```

### 3. Raise services

```bash
docker-compose up --build
```

The API will be available at: http&#x3A;//localhost:8000  
Documentacion Swagger: http&#x3A;//localhost:8000/docs

* * *

## Run migrations (first time)

Inside the container`api`:

```bash
docker-compose exec api alembic upgrade head
```

Or from your local environment (with the DB accessible):

```bash
alembic upgrade head
```

* * *

## Run tests

```bash
# Instalar dependencias
pip install -r requirements.txt

# Ejecutar tests
pytest tests/ -v
```

* * *

## Endpoints disponibles

### Health Check

| Method | Ruta      | Description    |
| ------ | --------- | -------------- |
| GET    | `/health` | Service status |

### Types of Incident

| Method | Ruta                                   | Description                      |
| ------ | -------------------------------------- | -------------------------------- |
| POST   | `/api/v1/tipos-incidencia`             | Create type                      |
| GET    | `/api/v1/tipos-incidencia`             | List with filters and pagination |
| GET    | `/api/v1/tipos-incidencia/{id}`        | See detail                       |
| PUT    | `/api/v1/tipos-incidencia/{id}`        | Update                           |
| PATCH  | `/api/v1/tipos-incidencia/{id}/estado` | Activate/Deactivate              |
| DELETE | `/api/v1/tipos-incidencia/{id}`        | Soft delete                      |

### Claims

| Method | Ruta                           | Description                      |
| ------ | ------------------------------ | -------------------------------- |
| POST   | `/api/v1/reclamos`             | Create claim                     |
| GET    | `/api/v1/reclamos`             | List with filters and pagination |
| GET    | `/api/v1/reclamos/{id}`        | Detail + history                 |
| PATCH  | `/api/v1/reclamos/{id}/estado` | Change status                    |
| PUT    | `/api/v1/reclamos/{id}`        | Edit claim                       |
| DELETE | `/api/v1/reclamos/{id}`        | Soft delete                      |

### Statistics (for reporting microservice)

| Method | Ruta                            | Description                    |
| ------ | ------------------------------- | ------------------------------ |
| GET    | `/api/v1/estadisticas/resumen`  | Totals by status/priority/type |
| GET    | `/api/v1/estadisticas/reclamos` | Full list without pagination   |

* * *

## Claim Status Transitions

```text
abierto -> en_proceso
en_proceso -> resuelto
en_proceso -> rechazado  (requiere motivo_rechazo)
resuelto -> cerrado
```

* * *

## Project structure

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

* * *

## Additional notes

-   Remember to create and configure the file`.env`before lifting services.
-   Files and folders like`__pycache__/`,`.env`,`venv/`, and temporary should be ignored in Git.
-   The Alembic migrations are in`alembic/versions/`.
-   The unit tests are in`tests/`.

* * *

## License

Prepared by DairXP
