from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_healthz():
    assert client.get("/healthz").json() == {"status": "ok"}


def test_task_lifecycle():
    created = client.post("/tasks", params={"title": "write CI"}).json()
    assert created["done"] is False
    done = client.post(f"/tasks/{created['id']}/done").json()
    assert done["done"] is True


def test_missing_task_returns_404():
    assert client.post("/tasks/9999/done").status_code == 404
