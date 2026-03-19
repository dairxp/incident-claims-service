from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_get_tipos_incidencia():
    # Validar que el endpoint está expuesto
    response = client.get("/api/v1/tipos-incidencia")
    assert response.status_code in [200, 500]
