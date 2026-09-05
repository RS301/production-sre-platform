from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "running"


def test_health():
    response = client.get("/health")
    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "healthy"


def test_ready():
    response = client.get("/ready")
    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "ready"


def test_metrics():
    response = client.get("/metrics")

    assert response.status_code == 200
    assert "http_requests_total" in response.text
