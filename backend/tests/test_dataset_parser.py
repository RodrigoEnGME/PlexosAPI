from pathlib import Path

from app.db import Base, SessionLocal, engine
from app.models import DatasetFile, DatasetRecord, Project, Tenant
from app.services.dataset_parser import _classify, import_folder, parse_sddp_control


def test_imports_text_and_binary_files(tmp_path: Path) -> None:
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    (tmp_path / "mgndur.dat").write_bytes(
        b"$version=3\r\n!Num Name Bus\r\n01  Central 1\r\n"
    )
    (tmp_path / "inflow.hdr").write_bytes(b"\x04\x00\x00\x00\x02\x00")
    db = SessionLocal()
    try:
        tenant = Tenant(name="Test", code="parser-test")
        db.add(tenant)
        db.flush()
        project = Project(name="Dataset", tenant_id=tenant.id)
        db.add(project)
        db.flush()
        result = import_folder(tmp_path, project.id, db)
        assert result == {"files": 2, "binary_files": 1, "errors": 0}
        assert db.query(DatasetFile).count() == 2
        assert db.query(DatasetRecord).count() == 3
        assert db.query(DatasetFile).filter(DatasetFile.file_kind == "binary").one().encoding is None
    finally:
        db.close()


def test_parses_sddp_control_values(tmp_path: Path) -> None:
    control = tmp_path / "sddp.dat"
    control.write_text(
        "Uruguay\nIDIOMA                       1  0=ING; 1=ESP\n"
        "ETAPA                        2  1=SEMANAL; 2=MENSUAL\n"
        "USA CRON. MANTENIMIENTO      1  0=USA IP; 1=USA CRONOG\n"
        "ANO INICIAL               2023\nNUMERO DE ETAPAS           228\n"
        "NUMERO DE SISTEMAS           1\nNUMERO DE SERIES            75\n"
        "NUMERO DE BLOQUES DEMANDA   21 1\n---------------- SISTEMAS --\n",
        encoding="utf-8",
    )
    descriptor = parse_sddp_control(control)
    assert descriptor["idioma"] == 1
    assert descriptor["language_code"] == "es"
    assert descriptor["etapa"] == 2
    assert descriptor["maintenance_mode"] == "schedule"
    assert descriptor["uses_maintenance_schedule"] is True
    assert descriptor["uses_programmed_outage_factor"] is False
    assert descriptor["ano inicial"] == 2023
    assert descriptor["numero de etapas"] == 228
    assert descriptor["numero de bloques demanda"] == [21, 1]


def test_classifies_utf16_sddp_control_as_text() -> None:
    control = "Uruguay\nIDIOMA 1\nETAPA 2\nUSA CRON. MANTENIMIENTO 1\n"
    assert _classify(Path("sddp.dat"), control.encode("utf-16")) == "control"
