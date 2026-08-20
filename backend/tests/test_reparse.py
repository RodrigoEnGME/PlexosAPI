from pathlib import Path

from app.db import Base, SessionLocal, engine
from app.models import AssetModification, Project, StudyRevision, Tenant
from app.services.reparse import reparse_revision_modifications


def test_reparse_revision_modifications_is_idempotent(tmp_path: Path) -> None:
    root = tmp_path / "source"
    root.mkdir()
    (root / "mgndxx.dat").write_text(
        "$version=3\n!d/mm/yyyy Num Name\n01/01/2024  489 NI-Trini_SOL               1   76.38       1.\n",
        encoding="latin-1",
    )
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    db = SessionLocal()
    try:
        tenant = Tenant(name="Reparse Test", code="reparse-test")
        db.add(tenant)
        db.flush()
        project = Project(name="Reparse", tenant_id=tenant.id)
        db.add(project)
        db.flush()
        revision = StudyRevision(project_id=project.id, revision_number=1, is_active=True)
        db.add(revision)
        db.flush()

        first = reparse_revision_modifications(revision, db, root)
        second = reparse_revision_modifications(revision, db, root)

        assert (first.deleted, first.inserted) == (0, 1)
        assert (second.deleted, second.inserted) == (1, 1)
        assert db.query(AssetModification).filter_by(revision_id=revision.id, source_code="489").count() == 1
    finally:
        db.close()
