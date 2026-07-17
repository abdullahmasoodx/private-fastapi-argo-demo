from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_home():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["message"] == "Private FastAPI Argo Demo is running"


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_add():
    response = client.get("/add?a=10&b=5")
    assert response.status_code == 200
    assert response.json()["result"] == 15


def test_subtract():
    response = client.get("/sub?a=10&b=5")
    assert response.status_code == 200
    assert response.json()["result"] == 5


def test_multiply():
    response = client.get("/mul?a=10&b=5")
    assert response.status_code == 200
    assert response.json()["result"] == 50
