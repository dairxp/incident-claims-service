# Claims and Incident Microservice

REST API for managing claims and incidents in the university administrative area. Built with FastAPI + PostgreSQL + SQLAlchemy.

Language: [Espanol](README.md) | **English**

---

## Tech stack

| Technology | Version |
|---|---|
| Python | 3.11+ |
| FastAPI | 0.115.5 |
| SQLAlchemy | 2.0.36 |
| PostgreSQL | 16 |
| Pydantic | 2.10.3 |
| Alembic | 1.14.0 |

---

## Run with Docker

### 1. Clone and enter the project folder

```bash
cd incident-claims-service
```

### 2. Create the `.env` file

```bash
cp .env.example .env
```

### 3. Start services

```bash
docker-compose up --build
```

API URL: http://localhost:8000  
Swagger docs: http://localhost:8000/docs

---

## Run migrations (first time)

Inside the `api` container:

```bash
docker-compose exec api alembic upgrade head
```

Or from your local environment (with DB access):

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

## Available endpoints

### Health Check

| Method | Path | Description |
|---|---|---|
| GET | `/health` | Service status |

### Incident Types

| Method | Path | Description |
|---|---|---|
| POST | `/api/v1/tipos-incidencia` | Create type |
| GET | `/api/v1/tipos-incidencia` | List with filters and pagination |
| GET | `/api/v1/tipos-incidencia/{id}` | Get detail |
| PUT | `/api/v1/tipos-incidencia/{id}` | Update |
| PATCH | `/api/v1/tipos-incidencia/{id}/estado` | Enable/Disable |
| DELETE | `/api/v1/tipos-incidencia/{id}` | Soft delete |

### Claims

| Method | Path | Description |
|---|---|---|
| POST | `/api/v1/reclamos` | Create claim |
| GET | `/api/v1/reclamos` | List with filters and pagination |
| GET | `/api/v1/reclamos/{id}` | Detail + status history |
| PATCH | `/api/v1/reclamos/{id}/estado` | Change status |
| PUT | `/api/v1/reclamos/{id}` | Edit claim |
| DELETE | `/api/v1/reclamos/{id}` | Soft delete |

### Statistics (for reporting service)

| Method | Path | Description |
|---|---|---|
| GET | `/api/v1/estadisticas/resumen` | Totals by status/priority/type |
| GET | `/api/v1/estadisticas/reclamos` | Full list without pagination |

---

## Claim state transitions

```text
abierto -> en_proceso
en_proceso -> resuelto
en_proceso -> rechazado  (requires motivo_rechazo)
resuelto -> cerrado
```

---

## Project structure

```text
incident-claims-service/
|- app/
|- alembic/
|- tests/
|- requirements.txt
|- Dockerfile
|- docker-compose.yml
|- alembic.ini
|- README.md
|- README.en.md
```

---

## Additional notes

- Make sure to create and configure `.env` before starting services.
- Ignore `__pycache__/`, `.env`, `venv/`, and temp files in Git.
- Alembic migrations are located in `alembic/versions/`.
- Unit tests are in `tests/`.

---

## License

Created by DairXP
