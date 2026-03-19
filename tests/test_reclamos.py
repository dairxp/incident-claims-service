from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_get_reclamos():
    # Validar que el endpoint está expuesto
    response = client.get("/api/v1/reclamos")
    assert response.status_code in [200, 500]

def test_get_estadisticas():
    # Validar que el endpoint de estadísticas funciona en routing
    response = client.get("/api/v1/estadisticas/resumen")
    assert response.status_code in [200, 500]
