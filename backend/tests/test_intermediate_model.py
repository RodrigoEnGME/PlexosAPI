from pathlib import Path

from app.db import Base, SessionLocal, engine
from app.models import AssetModification, Project, StudyMaintenance, StudyRevision, Tenant
from app.services.intermediate_model import build_intermediate_model
from app.services.snapshot import effective_snapshot
from app.services.study_descriptor import build_study_descriptor


def test_builds_intermediate_uruguay_model() -> None:
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    db = SessionLocal()
    try:
        tenant = Tenant(name="Intermediate Test", code="intermediate-test")
        db.add(tenant)
        db.flush()
        project = Project(name="UY revision", tenant_id=tenant.id)
        db.add(project)
        db.flush()
        revision = StudyRevision(project_id=project.id, revision_number=1, is_active=True)
        db.add(revision)
        db.flush()
        build_study_descriptor(project, Path("data/UY_SDDP"), db, revision.id)
        result = build_intermediate_model(Path("data/UY_SDDP"), revision, db)
        assert result["systems"] == 1
        assert result["buses"] >= 50
        assert result["assets"] >= 20
        assert result["circuits"] >= 80
        assert result["modifications"] > 0
        assert db.query(AssetModification).filter_by(entity_type="renewable").count() > 0
        assert result["maintenance"] > 0
        assert db.query(StudyMaintenance).count() > 100
        snapshot = effective_snapshot(revision, stage=1, block=1, db=db)
        assert snapshot["provenance"] == "intermediate database snapshot"
        assert snapshot["study"]["initial_year"] == 2023
        assert snapshot["study"]["stages"] == 228
        assert snapshot["study"]["blocks"] == 21
        assert len(snapshot["buses"]) >= 50
        assert snapshot["maintenance"]
        assert snapshot["maintenance"][0]["year"] == 2023
        future = next(item for item in snapshot["entities"] if item["source_code"] == "342")
        assert future["is_active"] is False
        later_snapshot = effective_snapshot(revision, stage=61, block=1, db=db)
        later_future = next(item for item in later_snapshot["entities"] if item["source_code"] == "399")
        assert later_future["is_active"] is True
    finally:
        db.close()
