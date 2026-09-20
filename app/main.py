import os

from fastapi import FastAPI, HTTPException

app = FastAPI(title="Task API", version=os.getenv("APP_VERSION", "dev"))

_tasks: dict[int, dict] = {}


@app.get("/healthz")
def healthz() -> dict:
    return {"status": "ok"}


@app.get("/version")
def version() -> dict:
    return {"version": app.version}


@app.post("/tasks", status_code=201)
def create_task(title: str) -> dict:
    task_id = len(_tasks) + 1
    _tasks[task_id] = {"id": task_id, "title": title, "done": False}
    return _tasks[task_id]


@app.get("/tasks")
def list_tasks() -> list[dict]:
    return list(_tasks.values())


@app.get("/tasks/{task_id}")
def get_task(task_id: int) -> dict:
    if task_id not in _tasks:
        raise HTTPException(status_code=404, detail="Task not found")
    return _tasks[task_id]


@app.post("/tasks/{task_id}/done")
def complete_task(task_id: int) -> dict:
    if task_id not in _tasks:
        raise HTTPException(status_code=404, detail="Task not found")
    _tasks[task_id]["done"] = True
    return _tasks[task_id]


@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int) -> None:
    if task_id not in _tasks:
        raise HTTPException(status_code=404, detail="Task not found")
    del _tasks[task_id]
