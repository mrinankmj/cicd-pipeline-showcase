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


def test_get_task():
    created = client.post("/tasks", params={"title": "read a task"}).json()
    fetched = client.get(f"/tasks/{created['id']}").json()
    assert fetched == created


def test_get_missing_task_returns_404():
    assert client.get("/tasks/9999").status_code == 404


def test_delete_task():
    created = client.post("/tasks", params={"title": "delete me"}).json()
    task_id = created["id"]
    assert client.delete(f"/tasks/{task_id}").status_code == 204
    assert client.get(f"/tasks/{task_id}").status_code == 404


def test_delete_missing_task_returns_404():
    assert client.delete("/tasks/9999").status_code == 404


def test_list_tasks_filters_by_done():
    created = client.post("/tasks", params={"title": "filter me"}).json()
    client.post(f"/tasks/{created['id']}/done")

    done_titles = [t["title"] for t in client.get("/tasks", params={"done": True}).json()]
    not_done_titles = [t["title"] for t in client.get("/tasks", params={"done": False}).json()]
    assert "filter me" in done_titles
    assert "filter me" not in not_done_titles


def test_list_tasks_paginates():
    for i in range(5):
        client.post("/tasks", params={"title": f"page-task-{i}"})

    page = client.get("/tasks", params={"limit": 2, "offset": 0}).json()
    assert len(page) == 2


def test_update_task_title():
    created = client.post("/tasks", params={"title": "old title"}).json()
    updated = client.patch(f"/tasks/{created['id']}", params={"title": "new title"}).json()
    assert updated["title"] == "new title"
    assert updated["id"] == created["id"]


def test_update_missing_task_returns_404():
    assert client.patch("/tasks/9999", params={"title": "x"}).status_code == 404
