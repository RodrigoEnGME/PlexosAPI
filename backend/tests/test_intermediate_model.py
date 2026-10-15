import json
from datetime import UTC, datetime
from pathlib import Path

from app.api.routes import get_asset_history
from app.db import Base, SessionLocal, engine
from app.models import (
    AssetModification,
    EnergyAsset,
    Project,
    StudyDescriptor,
    StudyMaintenance,
    StudyRenewableAssignment,
    StudyRevision,
    Tenant,
)
from app.services.input_catalog import (
    catalog_as_dict,
    load_input_dictionary,
    validate_input_dictionary,
)
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
        thermal_event = db.query(AssetModification).filter_by(entity_type="thermal").first()
        assert thermal_event is not None
        assert "plant_type" in json.loads(thermal_event.changed_fields_json)
        assert result["maintenance"] > 0
        assert result["thermal_details"] > 0
        assert result["hydro_details"] > 0
        assert result["renewable_assignments"] > 0
        assert db.query(StudyRenewableAssignment).count() > 0
        assert db.query(StudyMaintenance).count() > 100
        parsed_maintenance = db.query(StudyMaintenance).first()
        assert parsed_maintenance.family in {"PMHI", "PMTR"}
        assert parsed_maintenance.frequency in {"weekly", "monthly"}
        assert parsed_maintenance.system_code
        assert json.loads(parsed_maintenance.header_evidence_json)
        assert parsed_maintenance.measure_type in {1, 2}
        assert parsed_maintenance.unit_type in {1, 2, 3, 4}
        mot_maintenance = db.query(StudyMaintenance).filter_by(asset_type="thermal", source_code="101").first()
        assert mot_maintenance is not None
        assert mot_maintenance.measure_type == 1
        assert mot_maintenance.unit_type == 2
        assert mot_maintenance.frequency == "monthly"
        assert mot_maintenance.system_code == "ur"
        snapshot = effective_snapshot(revision, stage=1, block=1, db=db)
        assert snapshot["provenance"] == "intermediate database snapshot"
        assert snapshot["study"]["initial_year"] == 2023
        assert snapshot["study"]["stages"] == 228
        assert snapshot["study"]["blocks"] == 21
        assert len(snapshot["buses"]) >= 50
        assert snapshot["maintenance"]
        assert snapshot["maintenance"][0]["year"] == 2023
        mot_snapshot = next(item for item in snapshot["entities"] if item["source_code"] == "101" and item["asset_type"] == "thermal")
        assert mot_snapshot["capacity_available_mw"] == 80.0
        assert next(item for item in snapshot["entities"] if item["asset_type"] == "hydro")["technical_details"]["kind"] == "hydro"
        descriptor = db.query(StudyDescriptor).filter_by(revision_id=revision.id).one()
        assert json.loads(descriptor.descriptor_json)["maintenance_mode"] == "schedule"
        mot_batlle = db.query(EnergyAsset).filter_by(revision_id=revision.id, source_code="101", asset_type="thermal").one()
        mot_history = get_asset_history(project.id, mot_batlle.id, block=1, tenant_id=tenant.id, db=db)
        april_2023 = mot_history["series"][3]
        assert april_2023["maintenance_value"] == 70.0
        assert april_2023["capacity_available_mw"] == 24.0
        future = next(item for item in snapshot["entities"] if item["source_code"] == "342")
        assert future["is_active"] is False
        later_snapshot = effective_snapshot(revision, stage=61, block=1, db=db)
        later_future = next(item for item in later_snapshot["entities"] if item["source_code"] == "399")
        assert later_future["is_active"] is True
    finally:
        db.close()


def test_snapshot_uses_modified_installed_capacity_for_availability() -> None:
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    db = SessionLocal()
    try:
        tenant = Tenant(name="Capacity Test", code="capacity-test")
        db.add(tenant)
        db.flush()
        project = Project(name="Capacity study", tenant_id=tenant.id)
        db.add(project)
        db.flush()
        revision = StudyRevision(project_id=project.id, revision_number=1, status="ready", is_active=True)
        db.add(revision)
        db.flush()
        db.add(StudyDescriptor(
            project_id=project.id,
            revision_id=revision.id,
            source_file="sddp.dat",
            descriptor_json=json.dumps({"ano inicial": 2024, "numero de etapas": 24, "numero de bloques demanda": [1]}),
        ))
        asset = EnergyAsset(
            revision_id=revision.id,
            source_code="1",
            name="TEST UNIT",
            asset_type="thermal",
            technology="thermal",
            capacity_mw=100,
            lifecycle_status="existing",
            source_file="ctermi.dat",
            source_line=1,
        )
        db.add(asset)
        db.flush()
        db.add(AssetModification(
            revision_id=revision.id,
            entity_type="thermal",
            source_code="1",
            effective_date=datetime(2025, 1, 1, tzinfo=UTC),
            changed_fields_json=json.dumps({"name": "TEST UNIT", "capacity": 40}),
            source_file="mtermi.dat",
            source_line=2,
        ))
        db.commit()

        snapshot = effective_snapshot(revision, stage=13, block=1, db=db)
        entity = next(item for item in snapshot["entities"] if item["source_code"] == "1")
        assert entity["capacity_installed_mw"] == 40
        assert entity["capacity_maximum_mw"] == 40
        assert entity["capacity_available_mw"] == 40
    finally:
        db.close()


def test_loads_and_validates_documented_input_dictionary() -> None:
    path = Path(__file__).resolve().parents[2] / "data/20250207_Diccionario_SDDP_PLEXOS_v0.xlsx"
    entries = load_input_dictionary(path)
    validate_input_dictionary(entries)
    catalog = catalog_as_dict(path)

    assert len(entries) == 92
    assert catalog["source_file_count"] == 25
    assert entries[0].source_sheet == "Hoja1"
    assert entries[0].source_row == 2
    assert any(entry.source_file == "chidroxx.dat" and entry.attribute == "Potencia Instalada" for entry in entries)
    assert any(entry.source_file == "mhidroxx.dat" for entry in entries)
