# cicd-pipeline-showcase

A production-style CI/CD pipeline for a small FastAPI service, running entirely on free GitHub Actions.

## Pipeline

```
lint + test ──► build + Trivy scan ──► deploy to ephemeral kind cluster ──► push to GHCR
 (ruff, pytest)  (fails on HIGH/CRIT)   (rollout + smoke test)              (main only)
```

## API
Full CRUD on tasks: `POST /tasks`, `GET /tasks` (filter with `?done=`, page with `?limit=&offset=`), `GET /tasks/{id}`, `PATCH /tasks/{id}`, `POST /tasks/{id}/done`, `DELETE /tasks/{id}`.

## Highlights
- **Multi-stage Dockerfile**: small image, non-root user, healthcheck.
- **Shift-left security**: Trivy blocks vulnerable images before they ship.
- **Real end-to-end test**: every build is deployed to a throwaway Kubernetes cluster inside CI.
- **Immutable tags**: images tagged with the short commit SHA plus `latest`.
- **Least-privilege** workflow permissions; publishing uses the built-in `GITHUB_TOKEN` (no stored secrets).
- **Coverage-checked**: every test run reports line coverage for `app/`.

## Run locally
```bash
pip install -r requirements-dev.txt
pytest -q
uvicorn app.main:app --reload     # http://localhost:8000/docs
docker build -t task-api . && docker run -p 8000:8000 task-api
```
