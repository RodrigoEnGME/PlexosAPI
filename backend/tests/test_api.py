from fastapi.testclient import TestClient

from app.db import init_db
from app.main import app


def test_health() -> None:
    init_db()
    with TestClient(app) as client:
        response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_tenant_and_project_flow() -> None:
    init_db()
    with TestClient(app) as client:
        tenant = client.post("/api/tenants", json={"name": "GME Test", "code": "gme-test-run"})
        assert tenant.status_code == 201
        tenant_id = tenant.json()["id"]
        project = client.post(
            "/api/projects",
            headers={"X-Tenant-ID": str(tenant_id)},
            json={"name": "Uruguay baseline"},
        )
        assert project.status_code == 201
        projects = client.get("/api/projects", headers={"X-Tenant-ID": str(tenant_id)})
        assert projects.json()[0]["name"] == "Uruguay baseline"
