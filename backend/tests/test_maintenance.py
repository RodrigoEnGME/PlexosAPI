import json
from types import SimpleNamespace

from fastapi.testclient import TestClient

from app.db import Base, SessionLocal, engine, init_db
from app.main import app
from app.models import Project, StudyMaintenance, StudyRevision, Tenant
from app.services.availability import calculate_availability


def test_availability_uses_pm_exclusively_and_rejects_m3s() -> None:
    pm = SimpleNamespace(
        year=2024, asset_type="thermal", source_code="1", asset_name="UNIT",
        stage_values_json=json.dumps([50]), unit_type=2, measure_type=1,
    )
    result = calculate_availability(100, {"unit_count": 2, "short_term_outage_pct": 20, "historical_outage_pct": 40}, [pm], year=2024, stage_index=1, asset_name="UNIT", asset_type="thermal", source_code="1")
    assert result["available"] == 50
    assert result["source"] == "maintenance_plan"

    pm.unit_type = 4
    unresolved = calculate_availability(100, {"unit_count": 2, "short_term_outage_pct": 20}, [pm], year=2024, stage_index=1, asset_name="UNIT", asset_type="thermal", source_code="1")
    assert unresolved["available"] is None
    assert "m3/s" in unresolved["warning"]


def test_maintenance_without_applicable_year_is_unresolved() -> None:
    pm = SimpleNamespace(
        year=2023, asset_type="thermal", source_code="1", asset_name="UNIT",
        stage_values_json=json.dumps([50]), unit_type=2, measure_type=1,
    )
    result = calculate_availability(100, {"unit_count": 2, "short_term_outage_pct": 20}, [pm], year=2024, stage_index=1, asset_name="UNIT", asset_type="thermal", source_code="1")
    assert result["available"] is None
    assert "no applicable value" in result["warning"]


def test_maintenance_settings_are_tenant_scoped_and_selectable() -> None:
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    init_db()
    db = SessionLocal()
    tenant = Tenant(name="Maintenance API", code="maintenance-api")
    other = Tenant(name="Other tenant", code="other-maintenance-api")
    db.add_all([tenant, other])
    db.flush()
    project = Project(name="Settings study", tenant_id=tenant.id)
    db.add(project)
    db.flush()
    revision = StudyRevision(project_id=project.id, revision_number=1, status="ready", is_active=True)
    db.add(revision)
    db.flush()
    db.add(StudyMaintenance(revision_id=revision.id, asset_type="thermal", source_code="1", asset_name="UNIT", measure_type=1, unit_type=2, year=2024, stage_values_json=json.dumps([10]), source_file="pmtrmeur.dat", source_line=3))
    db.commit()
    project_id, revision_id, tenant_id, other_tenant_id = project.id, revision.id, tenant.id, other.id
    db.close()

    with TestClient(app) as client:
        response = client.put(f"/api/projects/{project_id}/revisions/{revision_id}/maintenance-settings", headers={"X-Tenant-ID": str(tenant_id)}, json={"availability_basis": "long_term"})
        assert response.status_code == 200
        assert response.json()["availability_basis"] == "long_term"
        review = client.get(f"/api/projects/{project_id}/maintenance-review", headers={"X-Tenant-ID": str(tenant_id)})
        assert review.status_code == 200
        assert review.json()["review_status"] == "pending"
        confirmed = client.post(f"/api/projects/{project_id}/revisions/{revision_id}/maintenance-settings/confirm", headers={"X-Tenant-ID": str(tenant_id)}, json={"availability_basis": "long_term", "review_status": "confirmed", "override": {"source_file": "pmtrmeur.dat", "measure_type": 1, "unit_type": 2}})
        assert confirmed.status_code == 200
        review = client.get(f"/api/projects/{project_id}/maintenance-review", headers={"X-Tenant-ID": str(tenant_id)})
        assert review.json()["review_status"] == "confirmed"
        assert review.json()["tables"][0]["review_status"] == "confirmed"
        assert client.get(f"/api/projects/{project_id}/maintenance-settings", headers={"X-Tenant-ID": str(other_tenant_id)}).status_code == 404
