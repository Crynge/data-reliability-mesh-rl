from fastapi.testclient import TestClient

from services.mesh_api.app.main import app


client = TestClient(app)


def test_health_endpoint() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_overview_endpoint() -> None:
    response = client.get("/api/overview")
    assert response.status_code == 200
    payload = response.json()
    assert "mesh_health_score" in payload
    assert payload["findings"]

