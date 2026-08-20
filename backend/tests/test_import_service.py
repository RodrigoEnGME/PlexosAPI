from pathlib import Path
from zipfile import ZipFile

from app.db import Base, SessionLocal, engine
from app.models import DatasetFile, ImportRun, Project, StudyRevision, Tenant
from app.services.import_service import _control_file, _safe_extract, import_zip, run_import_job


def test_zip_import_creates_separate_revision_artifact(tmp_path: Path) -> None:
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    source = tmp_path / "UY_SDDP"
    source.mkdir()
    (source / "sddp.dat").write_text(
        "Uruguay\nANO INICIAL               2023\nNUMERO DE ETAPAS           2\n"
        "NUMERO DE SISTEMAS           1\nNUMERO DE SERIES            1\n"
        "NUMERO DE BLOQUES DEMANDA   2 1\n---------------- SISTEMAS --\n",
        encoding="utf-8",
    )
    (source / "sistem.dat").write_text(" NUM NOME                 ID UnM\n   1 Uruguay              ur USD\n", encoding="utf-8")
    archive = tmp_path / "uy.zip"
    with ZipFile(archive, "w") as zipped:
        for path in source.iterdir():
            zipped.write(path, Path("UY_SDDP") / path.name)
    db = SessionLocal()
    try:
        tenant = Tenant(name="Import Test", code="import-test")
        db.add(tenant)
        db.flush()
        project = Project(name="ZIP project", tenant_id=tenant.id)
        db.add(project)
        db.flush()
        revision = import_zip(archive=archive, project=project, db=db, artifact_root=tmp_path / "artifacts")
        assert revision.status == "ready"
        assert revision.is_active is True
        assert Path(revision.source_archive_uri).exists()
        assert db.query(StudyRevision).count() == 1
        assert revision.import_run is not None
        assert revision.import_run.status == "completed"
        assert "Semantic mapping: 1 systems" in (revision.import_run.message or "")
        assert db.query(DatasetFile).filter_by(relative_path="UY_SDDP/sddp.dat").one().file_kind == "control"
    finally:
        db.close()


def test_zip_import_skips_orphaned_revision_directory(tmp_path: Path) -> None:
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    source = tmp_path / "UY_SDDP"
    source.mkdir()
    (source / "sddp.dat").write_text(
        "Uruguay\nANO INICIAL               2023\nNUMERO DE ETAPAS           2\n"
        "NUMERO DE SISTEMAS           1\nNUMERO DE SERIES            1\n"
        "NUMERO DE BLOQUES DEMANDA   2 1\n---------------- SISTEMAS --\n",
        encoding="utf-8",
    )
    (source / "sistem.dat").write_text(" NUM NOME                 ID UnM\n   1 Uruguay              ur USD\n", encoding="utf-8")
    archive = tmp_path / "uy.zip"
    with ZipFile(archive, "w") as zipped:
        for path in source.iterdir():
            zipped.write(path, Path("UY_SDDP") / path.name)
    artifact_root = tmp_path / "artifacts"
    orphan = artifact_root / "1" / "1" / "revision-1" / "source"
    orphan.mkdir(parents=True)
    db = SessionLocal()
    try:
        tenant = Tenant(name="Orphan Test", code="orphan-test")
        db.add(tenant)
        db.flush()
        project = Project(name="ZIP project", tenant_id=tenant.id)
        db.add(project)
        db.flush()
        revision = import_zip(archive=archive, project=project, db=db, artifact_root=artifact_root)
        assert revision.revision_number == 2
        assert Path(revision.source_archive_uri).parent.name == "revision-2"
        assert orphan.exists()
    finally:
        db.close()


def test_control_file_reports_missing_sddp_file(tmp_path: Path) -> None:
    (tmp_path / "README.txt").write_text("not an SDDP study", encoding="utf-8")
    try:
        _control_file(tmp_path)
    except FileNotFoundError as exc:
        assert "No sddp.dat control file found" in str(exc)
        assert "README.txt" in str(exc)
    else:
        raise AssertionError("missing control file should fail with a diagnostic")


def test_safe_extract_rejects_archive_entry_limit(tmp_path: Path, monkeypatch) -> None:
    archive = tmp_path / "many-files.zip"
    with ZipFile(archive, "w") as zipped:
        zipped.writestr("one.txt", "one")
        zipped.writestr("two.txt", "two")
    monkeypatch.setattr("app.services.import_service.settings.max_archive_entries", 1)
    (tmp_path / "extract").mkdir()
    try:
        _safe_extract(archive, tmp_path / "extract")
    except ValueError as exc:
        assert "too many entries" in str(exc)
    else:
        raise AssertionError("archive entry limit should fail")


def test_safe_extract_rejects_uncompressed_size_limit(tmp_path: Path, monkeypatch) -> None:
    archive = tmp_path / "large.zip"
    with ZipFile(archive, "w") as zipped:
        zipped.writestr("data.txt", "0123456789")
    monkeypatch.setattr("app.services.import_service.settings.max_archive_uncompressed_bytes", 5)
    (tmp_path / "extract").mkdir()
    try:
        _safe_extract(archive, tmp_path / "extract")
    except ValueError as exc:
        assert "too many bytes" in str(exc)
    else:
        raise AssertionError("archive size limit should fail")


def test_background_import_persists_missing_control_file_error(tmp_path: Path) -> None:
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    archive = tmp_path / "invalid.zip"
    source = tmp_path / "not-sddp.txt"
    source.write_text("not an SDDP study", encoding="utf-8")
    with ZipFile(archive, "w") as zipped:
        zipped.write(source, "README.txt")
    db = SessionLocal()
    try:
        tenant = Tenant(name="Job Test", code="job-test")
        db.add(tenant)
        db.flush()
        project = Project(name="Invalid ZIP", tenant_id=tenant.id)
        db.add(project)
        db.flush()
        run = ImportRun(project_id=project.id, source_path="queued.zip", status="queued")
        db.add(run)
        db.commit()
        run_import_job(run_id=run.id, project_id=project.id, archive=archive, artifact_root=tmp_path / "artifacts")
        db.expire_all()
        result = db.get(ImportRun, run.id)
        assert result is not None
        assert result.status == "failed"
        assert "No sddp.dat control file found" in (result.message or "")
    finally:
        db.close()
