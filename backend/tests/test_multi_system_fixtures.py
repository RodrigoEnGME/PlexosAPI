import json
from pathlib import Path

from app.db import Base, SessionLocal, engine
from app.models import (
    Project,
    StudyBusDemand,
    StudyCircuit,
    StudyDemand,
    StudyDescriptor,
    StudyRevision,
    StudySystem,
    Tenant,
)
from app.services.intermediate_model import build_intermediate_model
from app.services.study_descriptor import build_study_descriptor


def test_parses_peru_fixed_width_network_and_suffix_families() -> None:
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    db = SessionLocal()
    try:
        tenant = Tenant(name="PE fixture", code="pe-fixture")
        db.add(tenant)
        db.flush()
        project = Project(name="PE_BC", tenant_id=tenant.id)
        db.add(project)
        db.flush()
        revision = StudyRevision(project_id=project.id, revision_number=1, is_active=True)
        db.add(revision)
        db.flush()
        build_study_descriptor(project, Path("data/PE_BC"), db, revision.id)
        result = build_intermediate_model(Path("data/PE_BC"), revision, db)
        assert result["systems"] == 1
        assert result["buses"] == 172
        assert result["circuits"] == 250
        assert result["assets"] >= 292
        assert result["demands"] > 0
        assert db.query(StudyDemand).count() > 0
        assert result["bus_demands"] > 0
        assert db.query(StudyBusDemand).count() > 0
        assert result["batteries"] == 0
        descriptor = db.query(StudyDescriptor).filter_by(revision_id=revision.id).one()
        assert json.loads(descriptor.descriptor_json)["block_durations_hours"]
    finally:
        db.close()


def test_parses_crie_multi_system_network() -> None:
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    db = SessionLocal()
    try:
        tenant = Tenant(name="CRIE fixture", code="crie-fixture")
        db.add(tenant)
        db.flush()
        project = Project(name="CRIE Gatun", tenant_id=tenant.id)
        db.add(project)
        db.flush()
        revision = StudyRevision(project_id=project.id, revision_number=1, is_active=True)
        db.add(revision)
        db.flush()
        build_study_descriptor(project, Path("data/PA_202503_R25_1050_Gatun_en_BC02"), db, revision.id)
        result = build_intermediate_model(Path("data/PA_202503_R25_1050_Gatun_en_BC02"), revision, db)
        assert result["systems"] == 8
        assert result["buses"] == 279
        assert result["circuits"] == 472
        assert result["assets"] >= 800
        assert db.query(StudySystem).count() == 8
        assert db.query(StudyCircuit).count() == 472
        assert result["batteries"] == 3
    finally:
        db.close()


def test_parses_system_rows_with_variable_spacing(tmp_path: Path) -> None:
    root = tmp_path / "study"
    root.mkdir()
    (root / "sistem.dat").write_text(
        "NUM NOME ID UnM\n 1  PERU pe USD\n 2 COSTA RICA   cr USD\n",
        encoding="latin-1",
    )
    db = SessionLocal()
    try:
        tenant = Tenant(name="Spacing fixture", code="spacing-fixture")
        db.add(tenant)
        db.flush()
        project = Project(name="Spacing", tenant_id=tenant.id)
        db.add(project)
        db.flush()
        revision = StudyRevision(project_id=project.id, revision_number=1, is_active=True)
        db.add(revision)
        db.flush()
        from app.services.intermediate_model import _load_systems

        systems = _load_systems(root, revision, db)
        assert set(systems) == {"pe", "cr"}
        assert [system.name for system in systems.values()] == ["PERU", "COSTA RICA"]
    finally:
        db.close()
