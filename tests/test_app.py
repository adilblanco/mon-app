from fastapi.testclient import TestClient
from app.app import app

client = TestClient(app)


def test_root_returns_200():
    response = client.get("/")
    assert response.status_code == 200


def test_root_message():
    response = client.get("/")
    assert response.json()["message"] == "mon-app is running"


def test_health_ok():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_version_endpoint():
    response = client.get("/version")
    assert response.status_code == 200
    assert "version" in response.json()
