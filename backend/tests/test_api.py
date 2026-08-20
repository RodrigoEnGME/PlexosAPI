from datetime import UTC, datetime

from fastapi.testclient import TestClient

from app.db import SessionLocal, init_db
from app.main import app
from app.models import (
    Project,
    StudyAnalyticsJob,
    StudyBus,
    StudyBusDemand,
    StudyHourlyLoad,
    StudyLoadLevelMap,
    StudyRevision,
    StudySystem,
    Tenant,
)


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


def test_bus_demand_returns_as_of_dbf_block_curve() -> None:
    init_db()
    db = SessionLocal()
    tenant = Tenant(name="Demand Test", code="demand-test")
    db.add(tenant)
    db.flush()
    project = Project(name="Demand study", tenant_id=tenant.id)
    db.add(project)
    db.flush()
    revision = StudyRevision(project_id=project.id, revision_number=1, status="ready", is_active=True)
    db.add(revision)
    db.flush()
    system = StudySystem(revision_id=revision.id, code="uy", name="Uruguay")
    db.add(system)
    db.flush()
    db.add(StudyBus(revision_id=revision.id, system_id=system.id, source_code="304", name="Maldonado150", source_file="dbus.dat", source_line=4))
    db.add_all([
        StudyBusDemand(revision_id=revision.id, bus_code="304", demand_code="1", effective_date=datetime(2024, 1, 1, tzinfo=UTC), block=1, demand_mw=10, source_file="dbf021ur.dat", source_line=10),
        StudyBusDemand(revision_id=revision.id, bus_code="304", demand_code="1", effective_date=datetime(2024, 1, 1, tzinfo=UTC), block=2, demand_mw=20, source_file="dbf021ur.dat", source_line=11),
        StudyBusDemand(revision_id=revision.id, bus_code="304", demand_code="1", effective_date=datetime(2024, 2, 1, tzinfo=UTC), block=1, demand_mw=12, source_file="dbf021ur.dat", source_line=12),
        StudyLoadLevelMap(revision_id=revision.id, year=0, month=1, hour=1, load_level=1, source_file="hrbmap210.csv", source_line=2),
        StudyHourlyLoad(revision_id=revision.id, load_code="Uruguay", year=2024, month=1, hour=1, value_mw=100, source_file="hrloadur.dat", source_line=3),
    ])
    db.commit()
    project_id = project.id
    tenant_id = tenant.id
    db.close()

    with TestClient(app) as client:
        response = client.get(
            f"/api/projects/{project_id}/buses/304/demand?date=2024-01-01",
            headers={"X-Tenant-ID": str(tenant_id)},
        )
    assert response.status_code == 200
    payload = response.json()
    assert payload["authority"] == "DBF"
    assert payload["selected_date"] == "2024-01-01"
    assert [row["demand_mw"] for row in payload["records"]] == [10, 20]
    assert payload["hourly_formula"].startswith("HRLOAD aggregate")
    assert payload["hourly_series"][0]["demand_mw"] == 100


def test_analytics_status_reports_global_profile_progress() -> None:
    init_db()
    db = SessionLocal()
    tenant = Tenant(name="Analytics Test", code="analytics-status-test")
    db.add(tenant)
    db.flush()
    project = Project(name="Analytics study", tenant_id=tenant.id)
    db.add(project)
    db.flush()
    revision = StudyRevision(project_id=project.id, revision_number=1, status="ready", is_active=True)
    db.add(revision)
    db.flush()
    db.add(StudyAnalyticsJob(revision_id=revision.id, status="running", phase="profile statistics", progress=40, processed_assets=2, total_assets=5))
    db.commit()
    project_id = project.id
    tenant_id = tenant.id
    db.close()

    with TestClient(app) as client:
        response = client.get(f"/api/projects/{project_id}/analytics/status", headers={"X-Tenant-ID": str(tenant_id)})
    assert response.status_code == 200
    assert response.json() == {
        "status": "running",
        "phase": "profile statistics",
        "progress": 40,
        "processed_assets": 2,
        "total_assets": 5,
        "error": None,
    }
