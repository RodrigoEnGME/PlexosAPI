import hashlib
import json
import shutil
import threading
import zipfile
from pathlib import Path

from sqlalchemy.orm import Session

from app.db import SessionLocal
from app.models import ImportRun, Project, StudyAnalyticsJob, StudyDescriptor, StudyRevision
from app.services.analytics import run_analytics_job
from app.services.dataset_parser import import_folder
from app.services.intermediate_model import _files, build_intermediate_model
from app.services.study_descriptor import build_study_descriptor
from app.settings import settings

IMPORT_LOCK = threading.Lock()


def _safe_extract(archive: Path, destination: Path) -> None:
    destination_resolved = destination.resolve()
    with zipfile.ZipFile(archive) as zipped:
        members = zipped.infolist()
        if len(members) > settings.max_archive_entries:
            raise ValueError(
                f"ZIP contains too many entries ({len(members)}); "
                f"maximum is {settings.max_archive_entries}"
            )
        uncompressed_size = sum(member.file_size for member in members)
        if uncompressed_size > settings.max_archive_uncompressed_bytes:
            raise ValueError(
                f"ZIP expands to too many bytes ({uncompressed_size}); "
                f"maximum is {settings.max_archive_uncompressed_bytes}"
            )
        for member in members:
            target = (destination / member.filename).resolve()
            if target != destination_resolved and destination_resolved not in target.parents:
                raise ValueError(f"Unsafe ZIP member: {member.filename}")
        for member in members:
            zipped.extract(member, destination)


def _archive_hash(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _control_file(root: Path) -> Path:
    candidates = [path for path in root.rglob("*") if path.is_file() and path.name.lower() == "sddp.dat"]
    if not candidates:
        visible = sorted(path.relative_to(root).as_posix() for path in root.rglob("*") if path.is_file())[:20]
        raise FileNotFoundError(
            "No sddp.dat control file found in ZIP. "
            f"The archive may not be a complete SDDP study. Files seen: {', '.join(visible) or 'none'}"
        )
    return candidates[0]


def _find_file(root: Path, name: str) -> Path | None:
    return next((path for path in root.rglob("*") if path.is_file() and path.name.lower() == name.lower()), None)


def _progress(run: ImportRun, *, phase: str, progress: int, log: str, db: Session) -> None:
    try:
        payload = json.loads(run.message or "{}")
    except json.JSONDecodeError:
        payload = {}
    logs = payload.get("logs", [])
    logs.append(log)
    run.status = "running"
    run.message = json.dumps({"phase": phase, "progress": progress, "logs": logs}, ensure_ascii=False)
    db.commit()


def import_zip(*, archive: Path, project: Project, db: Session, artifact_root: Path, run: ImportRun | None = None) -> StudyRevision:
    revision_root = artifact_root / str(project.tenant_id) / str(project.id)
    revision_root.mkdir(parents=True, exist_ok=True)
    latest = db.query(StudyRevision.revision_number).filter(
        StudyRevision.project_id == project.id,
    ).order_by(StudyRevision.revision_number.desc()).first()
    revision_number = (latest[0] if latest else 0) + 1
    # A previous process can leave an artifact directory after failing before
    # the revision is committed. Never reuse that directory or its source tree.
    while (revision_root / f"revision-{revision_number}").exists():
        revision_number += 1
    revision_dir = revision_root / f"revision-{revision_number}"
    revision_dir.mkdir()
    stored_archive = revision_dir / archive.name
    shutil.copy2(archive, stored_archive)
    extracted = revision_dir / "source"
    extracted.mkdir()
    _safe_extract(stored_archive, extracted)
    if run is None:
        run = ImportRun(project_id=project.id, source_path=str(extracted), status="running")
        db.add(run)
        db.flush()
    else:
        run.source_path = str(extracted)
    _progress(run, phase="extracting", progress=10, log="Archive stored and extracted safely.", db=db)
    revision = StudyRevision(
        project_id=project.id, import_run_id=run.id, revision_number=revision_number,
        status="inspecting", source_archive_uri=str(stored_archive),
        source_archive_sha256=_archive_hash(stored_archive),
    )
    db.add(revision)
    db.flush()
    try:
        _progress(run, phase="inventory", progress=20, log="Scanning source files and detecting encodings.", db=db)
        import_folder(extracted, project.id, db, run, revision.id)
        control = _control_file(extracted)
        _progress(run, phase="inventory", progress=45, log=f"SDDP control file found: {control.relative_to(extracted).as_posix()}.", db=db)
        _progress(run, phase="descriptor", progress=55, log=f"Inventory complete: {run.files_processed} files, {run.files_binary} binary artifacts.", db=db)
        build_study_descriptor(project, extracted, db, revision.id)
        _progress(run, phase="mapping", progress=70, log="Building buses, circuits, assets and dated modifications.", db=db)
        result = build_intermediate_model(extracted, revision, db)
        descriptor_row = db.query(StudyDescriptor.descriptor_json).filter(
            StudyDescriptor.revision_id == revision.id,
        ).first()
        descriptor_payload = json.loads(descriptor_row[0]) if descriptor_row else {}
        expected_systems = descriptor_payload.get("numero de sistemas")
        if isinstance(expected_systems, int) and result["systems"] != expected_systems:
            warning = (
                f"Semantic mapping found {result['systems']} systems, "
                f"but SDDP.DAT declares {expected_systems}."
            )
            descriptor_payload.setdefault("warnings", []).append(warning)
            descriptor_record = db.query(StudyDescriptor).filter(StudyDescriptor.revision_id == revision.id).first()
            if descriptor_record:
                descriptor_record.descriptor_json = json.dumps(descriptor_payload, ensure_ascii=False)
                descriptor_record.warnings_json = json.dumps(descriptor_payload["warnings"], ensure_ascii=False)
            _progress(run, phase="quality", progress=80, log=f"Warning: {warning}", db=db)
        expected_families = (
            _files(extracted, "ctermi*.dat")
            + _files(extracted, "chidro*.dat")
            + _files(extracted, "cgnd*.dat")
        )
        if expected_families and result["assets"] == 0:
            raise ValueError("Semantic mapping produced zero assets despite generator configuration files being present.")
        if _find_file(extracted, "dbus.dat") and result["buses"] == 0:
            raise ValueError("Semantic mapping produced zero buses despite DBUS.DAT being present.")
        if _find_file(extracted, "dcirc.dat") and result["circuits"] == 0:
            raise ValueError("Semantic mapping produced zero circuits despite DCIRC.DAT being present.")
        _progress(run, phase="quality", progress=90, log=f"Semantic mapping: {result['systems']} systems, {result['assets']} assets, {result['buses']} buses, {result['circuits']} circuits.", db=db)
        revision.status = "ready"
        revision.is_active = True
        db.query(StudyRevision).filter(
            StudyRevision.project_id == project.id, StudyRevision.id != revision.id,
        ).update({StudyRevision.is_active: False})
        run.status = "completed"
        run.message = json.dumps({"phase": "completed", "progress": 100, "logs": json.loads(run.message or "{}").get("logs", []) + ["Study revision is ready and active."]}, ensure_ascii=False)
        db.commit()
        return revision
    except Exception as exc:
        revision.status = "failed"
        run.status = "failed"
        run.message = json.dumps({"phase": "failed", "progress": 100, "logs": json.loads(run.message or "{}").get("logs", []) + [f"Import failed: {exc}"]}, ensure_ascii=False)
        db.commit()
        raise


def run_import_job(*, run_id: int, project_id: int, archive: Path, artifact_root: Path) -> None:
    db = SessionLocal()
    try:
        run = db.get(ImportRun, run_id)
        project = db.get(Project, project_id)
        if run is None or project is None:
            return
        with IMPORT_LOCK:
            _progress(run, phase="queued", progress=1, log="Importer lock acquired; processing one SQLite import at a time.", db=db)
            revision = import_zip(archive=archive, project=project, db=db, artifact_root=artifact_root, run=run)
            job = StudyAnalyticsJob(revision_id=revision.id, status="pending", phase="queued")
            db.add(job)
            db.commit()
            analytics_thread = threading.Thread(target=run_analytics_job, args=(job.id,), daemon=True)
            analytics_thread.start()
    except Exception:  # noqa: BLE001
        # import_zip persists the failure details for the polling endpoint.
        db.rollback()
    finally:
        archive.unlink(missing_ok=True)
        db.close()
