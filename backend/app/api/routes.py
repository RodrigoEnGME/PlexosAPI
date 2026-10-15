import json
import tempfile
from datetime import datetime
from pathlib import Path
from statistics import mean, pstdev

from fastapi import (
    APIRouter,
    BackgroundTasks,
    Depends,
    File,
    Header,
    HTTPException,
    UploadFile,
    status,
)
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db import get_db
from app.models import (
    AssetModification,
    Conversion,
    DatasetFile,
    EnergyAsset,
    ImportRun,
    MaintenanceSetting,
    Project,
    StudyAnalyticsJob,
    StudyBus,
    StudyBusDemand,
    StudyDescriptor,
    StudyHourlyLoad,
    StudyHydroDetail,
    StudyHydroInflow,
    StudyLoadLevelMap,
    StudyMaintenance,
    StudyProfileStatistic,
    StudyRenewableHourlyProfile,
    StudyRenewableProfile,
    StudyRevision,
    StudySystem,
    StudyThermalDetail,
    Tenant,
)
from app.schemas import (
    ConversionRead,
    DatasetFileRead,
    ImportRunRead,
    ProjectCreate,
    ProjectRead,
    StudyDescriptorRead,
    StudyRevisionRead,
    TenantCreate,
    TenantRead,
    MaintenanceSettingsRead,
    MaintenanceSettingsWrite,
)
from app.services.encoding import detect_encoding
from app.services.import_service import run_import_job
from app.services.snapshot import (
    _maintenance_matches,
    _maintenance_value_is_valid,
    _modification_applies,
    _stage_date,
    effective_snapshot,
)
from app.services.availability import calculate_availability
from app.settings import settings

router = APIRouter()


def _profile_stats(values: list[float]) -> dict[str, float | int]:
    ordered = sorted(values)
    def percentile(fraction: float) -> float:
        position = (len(ordered) - 1) * fraction
        lower = int(position)
        upper = min(lower + 1, len(ordered) - 1)
        return ordered[lower] + (ordered[upper] - ordered[lower]) * (position - lower)
    return {"mean": mean(values), "p10": percentile(.1), "p25": percentile(.25), "p75": percentile(.75), "p90": percentile(.9), "min": ordered[0], "max": ordered[-1], "stddev": pstdev(values), "valid_count": len(values)}


def tenant_from_header(x_tenant_id: int | None = Header(default=None)) -> int:
    if x_tenant_id is None:
        raise HTTPException(status_code=400, detail="X-Tenant-ID header is required")
    return x_tenant_id


@router.get("/tenants", response_model=list[TenantRead], tags=["tenants"])
def list_tenants(db: Session = Depends(get_db)):  # noqa: B008
    return list(db.scalars(select(Tenant).order_by(Tenant.name)))


@router.post("/tenants", response_model=TenantRead, status_code=status.HTTP_201_CREATED, tags=["tenants"])
def create_tenant(payload: TenantCreate, db: Session = Depends(get_db)):  # noqa: B008
    tenant = Tenant(name=payload.name, code=payload.code)
    db.add(tenant)
    db.commit()
    db.refresh(tenant)
    return tenant


@router.get("/projects", response_model=list[ProjectRead], tags=["projects"])
def list_projects(tenant_id: int = Depends(tenant_from_header), db: Session = Depends(get_db)):  # noqa: B008
    return list(db.scalars(select(Project).where(Project.tenant_id == tenant_id).order_by(Project.name)))


@router.post("/projects", response_model=ProjectRead, status_code=status.HTTP_201_CREATED, tags=["projects"])
def create_project(
    payload: ProjectCreate,
    tenant_id: int = Depends(tenant_from_header),
    db: Session = Depends(get_db),  # noqa: B008
):
    if db.get(Tenant, tenant_id) is None:
        raise HTTPException(status_code=404, detail="Tenant not found")
    project = Project(name=payload.name, tenant_id=tenant_id)
    db.add(project)
    db.commit()
    db.refresh(project)
    return project


@router.post("/projects/{project_id}/conversions", response_model=ConversionRead, tags=["conversions"])
async def inspect_sddp_file(
    project_id: int,
    file: UploadFile = File(...),  # noqa: B008
    tenant_id: int = Depends(tenant_from_header),
    db: Session = Depends(get_db),  # noqa: B008
):
    project = db.scalar(select(Project).where(Project.id == project_id, Project.tenant_id == tenant_id))
    if project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    raw = await file.read()
    detection = detect_encoding(raw)
    conversion = Conversion(
        project_id=project_id,
        status="inspected",
        source_filename=file.filename or "unnamed.dat",
        detected_encoding=detection.encoding,
        diagnostics=json.dumps(detection.model_dump()),
    )
    db.add(conversion)
    db.commit()
    db.refresh(conversion)
    return conversion


@router.post("/projects/{project_id}/imports", response_model=ImportRunRead, status_code=status.HTTP_202_ACCEPTED, tags=["imports"])
async def upload_sddp_zip(
    project_id: int,
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),  # noqa: B008
    tenant_id: int = Depends(tenant_from_header),
    db: Session = Depends(get_db),  # noqa: B008
):
    project = db.scalar(select(Project).where(Project.id == project_id, Project.tenant_id == tenant_id))
    if project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    if not (file.filename or "").lower().endswith(".zip"):
        raise HTTPException(status_code=400, detail="Only ZIP imports are supported")
    temporary_path: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(prefix="sddp-upload-", suffix=".zip", delete=False) as temporary:
            temporary_path = Path(temporary.name)
            total = 0
            while chunk := await file.read(1024 * 1024):
                total += len(chunk)
                if total > settings.max_upload_bytes:
                    raise HTTPException(status_code=413, detail="Uploaded archive is too large")
                temporary.write(chunk)
        run = ImportRun(project_id=project_id, source_path=str(temporary_path), status="queued", message=json.dumps({"phase": "queued", "progress": 0, "logs": ["Upload received. Waiting for importer worker."]}))
        db.add(run)
        db.commit()
        db.refresh(run)
        background_tasks.add_task(run_import_job, run_id=run.id, project_id=project_id, archive=temporary_path, artifact_root=Path(settings.artifact_root))
        return run
    except Exception:
        if temporary_path:
            temporary_path.unlink(missing_ok=True)
        raise


@router.get("/projects/{project_id}/revisions", response_model=list[StudyRevisionRead], tags=["imports"])
def list_revisions(
    project_id: int,
    tenant_id: int = Depends(tenant_from_header),
    db: Session = Depends(get_db),  # noqa: B008
):
    project = db.scalar(select(Project).where(Project.id == project_id, Project.tenant_id == tenant_id))
    if project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    return list(db.scalars(select(StudyRevision).where(
        StudyRevision.project_id == project_id,
    ).order_by(StudyRevision.revision_number.desc())))


@router.post("/projects/{project_id}/revisions/{revision_id}/activate", response_model=StudyRevisionRead, tags=["imports"])
def activate_revision(
    project_id: int,
    revision_id: int,
    tenant_id: int = Depends(tenant_from_header),
    db: Session = Depends(get_db),  # noqa: B008
):
    project = db.scalar(select(Project).where(Project.id == project_id, Project.tenant_id == tenant_id))
    revision = db.scalar(select(StudyRevision).where(
        StudyRevision.id == revision_id,
        StudyRevision.project_id == project_id,
    ))
    if project is None or revision is None:
        raise HTTPException(status_code=404, detail="Project or revision not found")
    if revision.status not in {"ready", "parsed"}:
        raise HTTPException(status_code=409, detail="Revision is not ready")
    db.query(StudyRevision).filter(StudyRevision.project_id == project_id).update({StudyRevision.is_active: False})
    revision.is_active = True
    db.commit()
    db.refresh(revision)
    return revision


@router.get("/projects/{project_id}/files", response_model=list[DatasetFileRead], tags=["datasets"])
def list_dataset_files(
    project_id: int,
    tenant_id: int = Depends(tenant_from_header),
    db: Session = Depends(get_db),  # noqa: B008
):
    project = db.scalar(select(Project).where(Project.id == project_id, Project.tenant_id == tenant_id))
    if project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    return list(db.scalars(select(DatasetFile).where(DatasetFile.project_id == project_id).order_by(DatasetFile.relative_path)))


@router.get("/projects/{project_id}/imports", response_model=list[ImportRunRead], tags=["datasets"])
def list_imports(
    project_id: int,
    tenant_id: int = Depends(tenant_from_header),
    db: Session = Depends(get_db),  # noqa: B008
):
    project = db.scalar(select(Project).where(Project.id == project_id, Project.tenant_id == tenant_id))
    if project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    return list(db.scalars(select(ImportRun).where(ImportRun.project_id == project_id).order_by(ImportRun.created_at.desc())))


@router.get("/projects/{project_id}/imports/{run_id}", response_model=ImportRunRead, tags=["datasets"])
def get_import(
    project_id: int,
    run_id: int,
    tenant_id: int = Depends(tenant_from_header),
    db: Session = Depends(get_db),  # noqa: B008
):
    run = db.scalar(select(ImportRun).join(Project, Project.id == ImportRun.project_id).where(
        ImportRun.id == run_id, ImportRun.project_id == project_id, Project.tenant_id == tenant_id,
    ))
    if run is None:
        raise HTTPException(status_code=404, detail="Project or import not found")
    return run


@router.get("/projects/{project_id}/study", response_model=StudyDescriptorRead, tags=["study"])
def get_study(
    project_id: int,
    tenant_id: int = Depends(tenant_from_header),
    db: Session = Depends(get_db),  # noqa: B008
):
    project = db.scalar(select(Project).where(Project.id == project_id, Project.tenant_id == tenant_id))
    if project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    revision = db.scalar(select(StudyRevision).where(
        StudyRevision.project_id == project_id,
        StudyRevision.is_active.is_(True),
    ).order_by(StudyRevision.revision_number.desc()))
    descriptor = db.scalar(select(StudyDescriptor).where(
        StudyDescriptor.project_id == project_id,
        StudyDescriptor.revision_id == revision.id if revision else False,
    )) or db.scalar(select(StudyDescriptor).where(
        StudyDescriptor.project_id == project_id,
        StudyDescriptor.revision_id.is_(None),
    ).order_by(StudyDescriptor.created_at.desc()))
    if descriptor is None:
        raise HTTPException(status_code=404, detail="Study descriptor not found")
    return descriptor


@router.get("/projects/{project_id}/entities", tags=["visualizer"])
def list_visual_entities(
    project_id: int,
    stage: int = 1,
    block: int | None = 1,
    tenant_id: int = Depends(tenant_from_header),
    db: Session = Depends(get_db),  # noqa: B008
):
    project = db.scalar(select(Project).where(Project.id == project_id, Project.tenant_id == tenant_id))
    if project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    revision = db.scalar(select(StudyRevision).where(
        StudyRevision.project_id == project_id,
        StudyRevision.is_active.is_(True),
    ).order_by(StudyRevision.revision_number.desc()))
    if revision is None:
        return {"entities": [], "placed": 0, "unplaced": 0, "coordinate_policy": "intermediate-database"}
    snapshot = effective_snapshot(revision, stage=stage, block=block, db=db)
    entities = []
    for item in snapshot["entities"]:
        entities.append({
            "id": str(item["id"]), "name": item["name"],
            "technology": item["technology"] or item["asset_type"],
            "bus": int(item["bus_code"]) if item.get("bus_code") and str(item["bus_code"]).isdigit() else None,
            "capacity_mw": item["capacity_mw"], "operating_factor": item["operating_factor"],
            "technical_details": item.get("technical_details"),
            "lifecycle_status": item["lifecycle_status"],
            "is_active": item["is_active"],
            "modifications": item["modifications"],
            "source_file": item["source_file"], "source_line": item["source_line"],
            "latitude": item["latitude"], "longitude": item["longitude"],
            "coordinate_status": item["coordinate_status"],
        })
    return {
        "entities": entities,
        "circuits": snapshot["circuits"],
        "placed": sum(entity["latitude"] is not None and entity["longitude"] is not None for entity in entities),
        "unplaced": sum(entity["latitude"] is None or entity["longitude"] is None for entity in entities),
        "coordinate_policy": "intermediate-database",
    }


@router.get("/projects/{project_id}/snapshot", tags=["visualizer"])
def get_snapshot(
    project_id: int,
    stage: int = 1,
    block: int | None = 1,
    tenant_id: int = Depends(tenant_from_header),
    db: Session = Depends(get_db),  # noqa: B008
):
    project = db.scalar(select(Project).where(Project.id == project_id, Project.tenant_id == tenant_id))
    if project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    revision = db.scalar(select(StudyRevision).where(
        StudyRevision.project_id == project_id,
        StudyRevision.is_active.is_(True),
    ).order_by(StudyRevision.revision_number.desc()))
    if revision is None:
        raise HTTPException(status_code=404, detail="Active study revision not found")
    return effective_snapshot(revision, stage, block, db)


def _maintenance_settings_response(setting: MaintenanceSetting) -> dict[str, object]:
    return {"project_id": setting.project_id, "revision_id": setting.revision_id, "availability_basis": setting.availability_basis, "review_status": setting.review_status, "override": json.loads(setting.override_json or "{}")}


def _apply_maintenance_override(db: Session, revision_id: int, override: dict[str, object], review_status: str = "overridden") -> None:
    measure_type = override.get("measure_type")
    unit_type = override.get("unit_type")
    source_file = override.get("source_file")
    source_code = override.get("source_code")
    if measure_type not in {1, 2} or unit_type not in {1, 2, 3, 4} or not source_file:
        return
    rows = db.scalars(select(StudyMaintenance).where(StudyMaintenance.revision_id == revision_id)).all()
    for row in rows:
        if source_file and row.source_file != source_file:
            continue
        if source_code and row.source_code != str(source_code):
            continue
        row.measure_type = int(measure_type)
        row.unit_type = int(unit_type)
        row.interpretation_status = "overridden" if review_status == "overridden" else row.interpretation_status
        row.review_status = review_status


def _maintenance_review_status(rows: list[StudyMaintenance]) -> str:
    if not rows or any(row.review_status not in {"confirmed", "overridden"} for row in rows):
        return "pending"
    return "overridden" if any(row.review_status == "overridden" for row in rows) else "confirmed"


@router.get("/projects/{project_id}/maintenance-settings", response_model=MaintenanceSettingsRead, tags=["maintenance"])
def get_maintenance_settings(project_id: int, tenant_id: int = Depends(tenant_from_header), db: Session = Depends(get_db)):
    project = db.scalar(select(Project).where(Project.id == project_id, Project.tenant_id == tenant_id))
    if project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    setting = db.scalar(select(MaintenanceSetting).where(MaintenanceSetting.project_id == project_id, MaintenanceSetting.revision_id.is_(None)))
    if setting is None:
        setting = MaintenanceSetting(project_id=project_id, availability_basis="short_term", review_status="pending")
        db.add(setting)
        db.commit()
        db.refresh(setting)
    return _maintenance_settings_response(setting)


@router.put("/projects/{project_id}/maintenance-settings", response_model=MaintenanceSettingsRead, tags=["maintenance"])
def update_project_maintenance_settings(project_id: int, payload: MaintenanceSettingsWrite, tenant_id: int = Depends(tenant_from_header), db: Session = Depends(get_db)):
    project = db.scalar(select(Project).where(Project.id == project_id, Project.tenant_id == tenant_id))
    if project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    if payload.availability_basis not in {"short_term", "long_term"}:
        raise HTTPException(status_code=422, detail="availability_basis must be short_term or long_term")
    setting = db.scalar(select(MaintenanceSetting).where(MaintenanceSetting.project_id == project_id, MaintenanceSetting.revision_id.is_(None))) or MaintenanceSetting(project_id=project_id)
    setting.availability_basis = payload.availability_basis
    if payload.review_status is not None:
        setting.review_status = payload.review_status
    if payload.override is not None:
        setting.override_json = json.dumps(payload.override)
        if setting.revision_id:
            _apply_maintenance_override(db, revision_id=setting.revision_id, override=payload.override, review_status=payload.review_status or "overridden")
    db.add(setting)
    db.commit()
    db.refresh(setting)
    return _maintenance_settings_response(setting)


@router.put("/projects/{project_id}/revisions/{revision_id}/maintenance-settings", response_model=MaintenanceSettingsRead, tags=["maintenance"])
def update_maintenance_settings(project_id: int, revision_id: int, payload: MaintenanceSettingsWrite, tenant_id: int = Depends(tenant_from_header), db: Session = Depends(get_db)):
    project = db.scalar(select(Project).where(Project.id == project_id, Project.tenant_id == tenant_id))
    revision = db.scalar(select(StudyRevision).where(StudyRevision.id == revision_id, StudyRevision.project_id == project_id))
    if project is None or revision is None:
        raise HTTPException(status_code=404, detail="Project or revision not found")
    if payload.availability_basis not in {"short_term", "long_term"}:
        raise HTTPException(status_code=422, detail="availability_basis must be short_term or long_term")
    setting = db.scalar(select(MaintenanceSetting).where(MaintenanceSetting.revision_id == revision_id)) or MaintenanceSetting(project_id=project_id, revision_id=revision_id)
    setting.availability_basis = payload.availability_basis
    if payload.review_status is not None:
        setting.review_status = payload.review_status
    if payload.override is not None:
        setting.override_json = json.dumps(payload.override)
        _apply_maintenance_override(db, revision_id=revision_id, override=payload.override, review_status=payload.review_status or "overridden")
    db.add(setting)
    db.commit()
    db.refresh(setting)
    return _maintenance_settings_response(setting)


@router.get("/projects/{project_id}/maintenance-review", tags=["maintenance"])
def get_maintenance_review(project_id: int, revision_id: int | None = None, tenant_id: int = Depends(tenant_from_header), db: Session = Depends(get_db)):
    project = db.scalar(select(Project).where(Project.id == project_id, Project.tenant_id == tenant_id))
    if project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    revision = db.scalar(select(StudyRevision).where(StudyRevision.id == revision_id, StudyRevision.project_id == project_id)) if revision_id else db.scalar(select(StudyRevision).where(StudyRevision.project_id == project_id, StudyRevision.is_active.is_(True)).order_by(StudyRevision.revision_number.desc()))
    if revision is None:
        raise HTTPException(status_code=404, detail="Revision not found")
    setting = db.scalar(select(MaintenanceSetting).where(MaintenanceSetting.revision_id == revision.id)) or db.scalar(select(MaintenanceSetting).where(MaintenanceSetting.project_id == project_id, MaintenanceSetting.revision_id.is_(None)))
    rows = list(db.scalars(select(StudyMaintenance).where(StudyMaintenance.revision_id == revision.id).order_by(StudyMaintenance.source_file, StudyMaintenance.source_line)))
    if setting:
        saved_override = json.loads(setting.override_json or "{}")
        if saved_override.get("source_file"):
            saved_override = {str(saved_override["source_file"]): saved_override}
        for row in rows:
            if row.review_status == "pending" and row.source_file in saved_override:
                row.review_status = "overridden"
        db.commit()
    tables: dict[str, dict[str, object]] = {}
    for row in rows:
        table = tables.setdefault(row.source_file, {"source_file": row.source_file, "family": row.family, "frequency": row.frequency, "system_code": row.system_code, "review_status": "pending", "examples": []})
        table["review_status"] = "overridden" if table["review_status"] == "overridden" or row.review_status == "overridden" else "confirmed" if table["review_status"] == "confirmed" and row.review_status == "confirmed" else row.review_status
        examples = table["examples"]
        if isinstance(examples, list) and len(examples) < 2 and any(float(value) != 0 for value in json.loads(row.stage_values_json)):
            examples.append({"source_code": row.source_code, "asset_name": row.asset_name, "source_line": row.source_line, "measure_type": row.measure_type, "unit_type": row.unit_type, "values": json.loads(row.stage_values_json)[:3], "warnings": json.loads(row.warnings_json), "header_evidence": json.loads(row.header_evidence_json or "{}"), "interpretation_status": row.interpretation_status})
    review_status = _maintenance_review_status(rows)
    if setting and setting.review_status != review_status:
        setting.review_status = review_status
        db.commit()
    return {"project_id": project_id, "revision_id": revision.id, "review_status": review_status, "availability_basis": setting.availability_basis if setting else "short_term", "tables": list(tables.values())}


@router.post("/projects/{project_id}/revisions/{revision_id}/maintenance-settings/confirm", response_model=MaintenanceSettingsRead, tags=["maintenance"])
def confirm_maintenance_settings(project_id: int, revision_id: int, payload: MaintenanceSettingsWrite | None = None, tenant_id: int = Depends(tenant_from_header), db: Session = Depends(get_db)):
    project = db.scalar(select(Project).where(Project.id == project_id, Project.tenant_id == tenant_id))
    revision = db.scalar(select(StudyRevision).where(StudyRevision.id == revision_id, StudyRevision.project_id == project_id))
    if project is None or revision is None:
        raise HTTPException(status_code=404, detail="Project or revision not found")
    setting = db.scalar(select(MaintenanceSetting).where(MaintenanceSetting.revision_id == revision_id)) or MaintenanceSetting(project_id=project_id, revision_id=revision_id)
    if payload and payload.override is not None:
        existing_override = json.loads(setting.override_json or "{}")
        source_file = payload.override.get("source_file")
        if source_file:
            existing_override[str(source_file)] = payload.override
        setting.override_json = json.dumps(existing_override)
        _apply_maintenance_override(db, revision_id=revision_id, override=payload.override, review_status=payload.review_status or "overridden")
    if payload and payload.availability_basis in {"short_term", "long_term"}:
        setting.availability_basis = payload.availability_basis
    rows = list(db.scalars(select(StudyMaintenance).where(StudyMaintenance.revision_id == revision_id)))
    setting.review_status = _maintenance_review_status(rows)
    setting.confirmed_at = datetime.utcnow()
    db.add(setting)
    db.commit()
    db.refresh(setting)
    return _maintenance_settings_response(setting)


@router.get("/projects/{project_id}/buses/{bus_code}/demand", tags=["visualizer"])
def get_bus_demand(
    project_id: int,
    bus_code: str,
    date: str | None = None,
    year: int | None = None,
    month: int | None = None,
    block: int | None = None,
    demand_code: str | None = None,
    tenant_id: int = Depends(tenant_from_header),
    db: Session = Depends(get_db),  # noqa: B008
):
    """Return the authoritative DBF block curve as-of a selected date.

    DBF is kept explicit here: DEME is aggregate and DBUS is a fallback
    snapshot value, so neither is silently mixed into a bus-level curve.
    """
    project = db.scalar(select(Project).where(Project.id == project_id, Project.tenant_id == tenant_id))
    revision = db.scalar(select(StudyRevision).where(
        StudyRevision.project_id == project_id,
        StudyRevision.is_active.is_(True),
    ).order_by(StudyRevision.revision_number.desc()))
    bus = db.scalar(select(StudyBus).where(StudyBus.revision_id == (revision.id if revision else -1), StudyBus.source_code == bus_code))
    if project is None or revision is None or bus is None:
        raise HTTPException(status_code=404, detail="Bus not found")

    query = select(StudyBusDemand).where(
        StudyBusDemand.revision_id == revision.id,
        StudyBusDemand.bus_code == bus_code,
    )
    all_rows = list(db.scalars(query.order_by(StudyBusDemand.effective_date, StudyBusDemand.block)))
    available_dates = sorted({row.effective_date.date().isoformat() for row in all_rows})
    available_blocks = sorted({row.block for row in all_rows})
    demand_codes = sorted({row.demand_code for row in all_rows})
    if year is not None:
        all_rows = [row for row in all_rows if row.effective_date.year == year]
    if month is not None:
        all_rows = [row for row in all_rows if row.effective_date.month == month]
    if block is not None:
        all_rows = [row for row in all_rows if row.block == block]
    if demand_code is not None:
        all_rows = [row for row in all_rows if row.demand_code == demand_code]

    selected_date: datetime | None = None
    requested_date: datetime | None = None
    if date:
        try:
            requested_date = datetime.fromisoformat(date).replace(tzinfo=None)
        except ValueError as exc:
            raise HTTPException(status_code=400, detail="date must use ISO format YYYY-MM-DD") from exc
        selected_date = max((row.effective_date for row in all_rows if row.effective_date <= requested_date), default=None)
    elif all_rows:
        selected_date = max(row.effective_date for row in all_rows)
    if selected_date is not None:
        all_rows = [row for row in all_rows if row.effective_date == selected_date]

    records = [
        {
            "bus_code": row.bus_code,
            "demand_code": row.demand_code,
            "effective_date": row.effective_date.date().isoformat(),
            "block": row.block,
            "demand_mw": row.demand_mw,
            "source_file": row.source_file,
            "source_line": row.source_line,
            "value_kind": "input",
        }
        for row in sorted(all_rows, key=lambda item: item.block)
    ]
    warnings = []
    if not records:
        fallback = json.loads(bus.demand_block_mw_json or "{}")
        if fallback:
            records = [
                {"bus_code": bus_code, "demand_code": None, "effective_date": None, "block": int(key), "demand_mw": value, "source_file": bus.source_file, "source_line": bus.source_line, "value_kind": "input"}
                for key, value in sorted(fallback.items(), key=lambda item: int(item[0]))
            ]
            warnings.append("DBF demand is unavailable; values come from DBUS embedded block fields.")
        else:
            warnings.append("No DBF or DBUS demand value is available for this bus and filter.")
    hourly_series = []
    hourly_formula = None
    target_date = requested_date or selected_date
    system = db.get(StudySystem, bus.system_id) if bus.system_id else None
    if target_date and system:
        hourly_rows = list(db.scalars(select(StudyHourlyLoad).where(
            StudyHourlyLoad.revision_id == revision.id,
            StudyHourlyLoad.year == target_date.year,
            StudyHourlyLoad.month == target_date.month,
        ).order_by(StudyHourlyLoad.hour)))
        level_rows = list(db.scalars(select(StudyLoadLevelMap).where(
            StudyLoadLevelMap.revision_id == revision.id,
            StudyLoadLevelMap.month == target_date.month,
        )))
        level_by_hour = {row.hour: row.load_level for row in level_rows}
        load_values = {(row.load_code.casefold(), row.hour): row.value_mw for row in hourly_rows}
        load_codes = {row.load_code.casefold() for row in hourly_rows}
        direct_load = bus.name.casefold() in load_codes and bus.name.casefold() != system.name.casefold()
        system_bus_codes = [row.source_code for row in db.scalars(select(StudyBus).where(StudyBus.revision_id == revision.id, StudyBus.system_id == bus.system_id))]
        bus_names = {row.source_code: row.name for row in db.scalars(select(StudyBus).where(StudyBus.revision_id == revision.id, StudyBus.system_id == bus.system_id))}
        weight_rows = list(db.scalars(select(StudyBusDemand).where(StudyBusDemand.revision_id == revision.id, StudyBusDemand.bus_code.in_(system_bus_codes))))
        latest_weights: dict[tuple[str, int], tuple[datetime, float]] = {}
        for row in weight_rows:
            key = (row.bus_code, row.block)
            current = latest_weights.get(key)
            if current is None or row.effective_date >= current[0]:
                latest_weights[key] = (row.effective_date, float(row.demand_mw or 0))
        for raw_hour in range((target_date.day - 1) * 24 + 1, target_date.day * 24 + 1):
            load_level = level_by_hour.get(raw_hour)
            if load_level is None or (block is not None and load_level != block):
                continue
            if direct_load:
                value = load_values.get((bus.name.casefold(), raw_hour))
                hourly_formula = "HRLOAD direct load column by node"
            else:
                aggregate = load_values.get((system.name.casefold(), raw_hour))
                excluded = {name.casefold() for code, name in bus_names.items() if name.casefold() in load_codes and name.casefold() != system.name.casefold()}
                denominator = sum(value for (code, level), (_, value) in latest_weights.items() if level == load_level and bus_names.get(code, "").casefold() not in excluded)
                numerator = latest_weights.get((bus_code, load_level), (None, 0))[1]
                value = aggregate * numerator / denominator if aggregate is not None and denominator else None
                hourly_formula = "HRLOAD aggregate × DBF block weight / non-elastic DBF block total"
            if value is not None:
                hourly_series.append({"period": raw_hour - (target_date.day - 1) * 24, "source_hour": raw_hour, "load_level": load_level, "demand_mw": value, "value_kind": "derived"})
        if not hourly_series:
            warnings.append("HRLOAD/HRBMAP hourly curve is unavailable for the selected year, month, node or block.")
    elif target_date:
        warnings.append("Hourly demand requires a resolved system and HRLOAD/HRBMAP inputs.")
    return {
        "bus_code": bus_code,
        "bus_name": bus.name,
        "authority": "DBF" if any(row["source_file"].lower().startswith("dbf") for row in records) else "DBUS" if records else None,
        "selected_date": selected_date.date().isoformat() if selected_date else None,
        "curve_date": target_date.date().isoformat() if target_date else None,
        "available_dates": available_dates,
        "available_blocks": available_blocks,
        "demand_codes": demand_codes,
        "hourly_series": hourly_series,
        "hourly_formula": hourly_formula,
        "records": records,
        "summary": {
            "total_mw": sum(float(row["demand_mw"] or 0) for row in records),
            "peak_mw": max((float(row["demand_mw"] or 0) for row in records), default=0),
            "block_count": len(records),
        },
        "warnings": warnings,
        "provenance": "StudyBusDemand / DBF input records; DBUS only as explicit fallback",
    }


@router.get("/projects/{project_id}/entities/{source_code}/history", tags=["visualizer"])
def get_entity_history(
    project_id: int,
    source_code: str,
    block: int | None = 1,
    tenant_id: int = Depends(tenant_from_header),
    db: Session = Depends(get_db),  # noqa: B008
):
    project = db.scalar(select(Project).where(Project.id == project_id, Project.tenant_id == tenant_id))
    if project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    revision = db.scalar(select(StudyRevision).where(
        StudyRevision.project_id == project_id,
        StudyRevision.is_active.is_(True),
    ).order_by(StudyRevision.revision_number.desc()))
    if revision is None:
        raise HTTPException(status_code=404, detail="Active study revision not found")
    descriptor = db.scalar(select(StudyDescriptor).where(StudyDescriptor.revision_id == revision.id))
    metadata = json.loads(descriptor.descriptor_json) if descriptor else {}
    stages = int(metadata.get("numero de etapas", 0) or 0)
    if stages < 1:
        raise HTTPException(status_code=422, detail="Study has no temporal stages")
    history = []
    for stage in range(1, stages + 1):
        snapshot = effective_snapshot(revision, stage, block, db)
        entity = next((item for item in snapshot["entities"] if item["source_code"] == source_code), None)
        if entity is not None:
            history.append({
                "stage": stage,
                "as_of": snapshot["as_of"],
                "lifecycle_status": entity["lifecycle_status"],
                "is_active": entity["is_active"],
                "capacity_installed_mw": entity.get("capacity_installed_mw"),
                 "capacity_maximum_mw": entity.get("capacity_maximum_mw"),
                 "capacity_available_mw": entity.get("capacity_available_mw"),
                 "availability_source": entity.get("availability_source"),
                 "availability_basis": entity.get("availability_basis"),
                 "availability_warning": entity.get("availability_warning"),
                 "has_maintenance_plan": entity.get("has_maintenance_plan"),
                "maintenance_value": entity.get("maintenance_value"),
                "maintenance_type": entity.get("maintenance_type"),
                "maintenance_unit": entity.get("maintenance_unit"),
                "value_kind": "derived",
            })
    if not history:
        raise HTTPException(status_code=404, detail="Entity not found")
    return {"source_code": source_code, "frequency": "weekly" if metadata.get("etapa") == 1 else "monthly", "series": history, "provenance": "intermediate database snapshot"}


@router.get("/projects/{project_id}/assets/{asset_id}/history", tags=["visualizer"])
def get_asset_history(
    project_id: int,
    asset_id: int,
    block: int | None = 1,
    tenant_id: int = Depends(tenant_from_header),
    db: Session = Depends(get_db),  # noqa: B008
):
    project = db.scalar(select(Project).where(Project.id == project_id, Project.tenant_id == tenant_id))
    revision = db.scalar(select(StudyRevision).where(StudyRevision.project_id == project_id, StudyRevision.is_active.is_(True)).order_by(StudyRevision.revision_number.desc()))
    asset = db.scalar(select(EnergyAsset).where(EnergyAsset.id == asset_id, EnergyAsset.revision_id == (revision.id if revision else -1)))
    if project is None or revision is None or asset is None:
        raise HTTPException(status_code=404, detail="Asset not found")
    descriptor = db.scalar(select(StudyDescriptor).where(StudyDescriptor.revision_id == revision.id))
    metadata = json.loads(descriptor.descriptor_json) if descriptor else {}
    initial_year = int(metadata.get("ano inicial", 2023))
    stages = int(metadata.get("numero de etapas", 0) or 0)
    weekly = metadata.get("etapa") == 1
    modifications = [item for item in db.scalars(select(AssetModification).where(AssetModification.revision_id == revision.id, AssetModification.entity_type == asset.asset_type, AssetModification.source_code == asset.source_code).order_by(AssetModification.effective_date, AssetModification.sequence)) if _modification_applies(asset.name, item)]
    maintenances = list(db.scalars(select(StudyMaintenance).where(StudyMaintenance.revision_id == revision.id, StudyMaintenance.asset_type == asset.asset_type, StudyMaintenance.source_code == asset.source_code)))
    setting = db.scalar(select(MaintenanceSetting).where(MaintenanceSetting.revision_id == revision.id)) or db.scalar(select(MaintenanceSetting).where(MaintenanceSetting.project_id == project_id, MaintenanceSetting.revision_id.is_(None)))
    availability_basis = setting.availability_basis if setting else "short_term"
    detail = None
    if asset.asset_type == "thermal":
        detail = db.scalar(select(StudyThermalDetail).where(StudyThermalDetail.revision_id == revision.id, StudyThermalDetail.source_code == asset.source_code))
    elif asset.asset_type == "hydro":
        detail = db.scalar(select(StudyHydroDetail).where(StudyHydroDetail.revision_id == revision.id, StudyHydroDetail.source_code == asset.source_code))
    system_code = db.scalar(select(StudySystem.code).where(StudySystem.id == asset.system_id)) if asset.system_id else None
    system_country_code = db.scalar(select(StudySystem.country_code).where(StudySystem.id == asset.system_id)) if asset.system_id else None
    current_capacity = asset.capacity_mw or 0.0
    operating_factor = asset.operating_factor
    lifecycle = asset.lifecycle_status
    series = []
    for stage in range(1, stages + 1):
        date = _stage_date(stage, initial_year)
        stage_events = []
        comparison_date = date.replace(tzinfo=None)
        for event in [item for item in modifications if item.effective_date and item.effective_date <= comparison_date]:
            payload = json.loads(event.changed_fields_json)
            if payload.get("capacity") is not None:
                current_capacity = float(payload["capacity"])
            if payload.get("factor") is not None:
                operating_factor = float(payload["factor"])
            if payload.get("existing") is not None:
                lifecycle = "future" if str(payload["existing"]) == "1" else "existing"
            if payload.get("plant_type") is not None:
                lifecycle = "future" if str(payload["plant_type"]) == "1" else "existing"
            if event.effective_date.date() == date.date():
                stage_events.append({"kind": "modification", "source_file": event.source_file, "source_line": event.source_line, "effective_date": event.effective_date.date().isoformat(), "fields": payload})
        # Dated capacity changes alter the installed capacity for this stage;
        # maintenance and outage factors are applied to that effective value.
        maximum = float(current_capacity or getattr(detail, "max_generation_mw", None) or 0.0)
        stage_index = stage if weekly else date.month
        detail_values = {"unit_count": getattr(detail, "unit_count", None), "short_term_outage_pct": getattr(detail, "short_term_outage_pct", None), "historical_outage_pct": getattr(detail, "historical_outage_pct", None)}
        availability = calculate_availability(maximum, detail_values, maintenances, year=date.year, stage_index=stage_index, basis=availability_basis, asset_name=asset.name, asset_type=asset.asset_type, source_code=asset.source_code, system_code=system_code, system_country_code=system_country_code)
        maintenance_item = availability["maintenance"]
        maintenance_value = availability["value"]
        maintenance_type = maintenance_item.measure_type if maintenance_item else None
        maintenance_unit = maintenance_item.unit_type if maintenance_item else None
        if maintenance_item:
            event = {"kind": "maintenance", "source_file": maintenance_item.source_file, "source_line": maintenance_item.source_line, "effective_date": date.date().isoformat(), "value": maintenance_value, "measure_type": maintenance_type, "unit_type": maintenance_unit}
            if availability["warning"]:
                event["warning"] = availability["warning"]
            stage_events.append(event)
        series.append({"stage": stage, "as_of": date.date().isoformat(), "year": date.year, "month": date.month, "lifecycle_status": lifecycle, "is_active": lifecycle == "existing" and current_capacity > 0, "capacity_installed_mw": current_capacity, "capacity_maximum_mw": maximum, "capacity_available_mw": availability["available"] if lifecycle == "existing" else 0, "availability_source": availability["source"], "availability_basis": availability_basis if availability["source"].endswith("outage_index") else None, "availability_warning": availability["warning"], "has_maintenance_plan": availability["has_maintenance_plan"], "operating_factor": operating_factor, "maintenance_value": maintenance_value, "maintenance_type": maintenance_type, "maintenance_unit": maintenance_unit, "events": stage_events, "value_kind": "derived"})
    return {"asset_id": asset_id, "frequency": "weekly" if weekly else "monthly", "series": series, "provenance": "targeted intermediate database history"}


@router.get("/projects/{project_id}/renewable-profiles/{source_code}/statistics", tags=["visualizer"])
def get_renewable_profile_statistics(
    project_id: int,
    source_code: str,
    stage: int | None = None,
    block: int | None = None,
    tenant_id: int = Depends(tenant_from_header),
    db: Session = Depends(get_db),  # noqa: B008
):
    project = db.scalar(select(Project).where(Project.id == project_id, Project.tenant_id == tenant_id))
    if project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    revision = db.scalar(select(StudyRevision).where(StudyRevision.project_id == project_id, StudyRevision.is_active.is_(True)).order_by(StudyRevision.revision_number.desc()))
    if revision is None:
        raise HTTPException(status_code=404, detail="Active study revision not found")
    query = select(StudyRenewableProfile).where(StudyRenewableProfile.revision_id == revision.id, StudyRenewableProfile.source_code == source_code)
    if stage is not None:
        query = query.where(StudyRenewableProfile.stage == stage)
    if block is not None:
        query = query.where(StudyRenewableProfile.block == block)
    values = [item.value_pu for item in db.scalars(query)]
    if not values:
        raise HTTPException(status_code=404, detail="Renewable input profile not found")
    ordered = sorted(values)
    def percentile(fraction: float) -> float:
        position = (len(ordered) - 1) * fraction
        lower = int(position)
        upper = min(lower + 1, len(ordered) - 1)
        return ordered[lower] + (ordered[upper] - ordered[lower]) * (position - lower)
    return {"source_code": source_code, "unit": "p.u.", "value_kind": "derived", "statistics": {"mean": mean(values), "p10": percentile(0.10), "p90": percentile(0.90), "min": ordered[0], "max": ordered[-1], "stddev": pstdev(values), "valid_count": len(values)}, "filters": {"stage": stage, "block": block}, "provenance": "derived from persisted renewable input profiles"}


@router.get("/projects/{project_id}/renewable-hourly/{source_code}/statistics", tags=["visualizer"])
def get_renewable_hourly_statistics(
    project_id: int,
    source_code: str,
    month: int | None = None,
    scenario: int | None = None,
    tenant_id: int = Depends(tenant_from_header),
    db: Session = Depends(get_db),  # noqa: B008
):
    project = db.scalar(select(Project).where(Project.id == project_id, Project.tenant_id == tenant_id))
    if project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    revision = db.scalar(select(StudyRevision).where(StudyRevision.project_id == project_id, StudyRevision.is_active.is_(True)).order_by(StudyRevision.revision_number.desc()))
    if revision is None:
        raise HTTPException(status_code=404, detail="Active study revision not found")
    asset = db.scalar(select(EnergyAsset).where(EnergyAsset.revision_id == revision.id, EnergyAsset.source_code == source_code))
    profile_codes = {source_code}
    if asset:
        profile_codes.update({asset.name, asset.name.replace(" ", "_")})
    query = select(StudyRenewableHourlyProfile).where(StudyRenewableHourlyProfile.revision_id == revision.id, StudyRenewableHourlyProfile.source_code.in_(profile_codes))
    if month is not None:
        query = query.where(StudyRenewableHourlyProfile.month == month)
    if scenario is not None:
        query = query.where(StudyRenewableHourlyProfile.scenario == scenario)
    grouped: dict[int, list[float]] = {}
    for item in db.scalars(query):
        grouped.setdefault(item.hour, []).append(item.value_pu)
    if not grouped:
        raise HTTPException(status_code=404, detail="Renewable hourly input profile not found")
    def stats(values: list[float]) -> dict[str, float | int]:
        ordered = sorted(values)
        def percentile(fraction: float) -> float:
            position = (len(ordered) - 1) * fraction
            lower = int(position)
            upper = min(lower + 1, len(ordered) - 1)
            return ordered[lower] + (ordered[upper] - ordered[lower]) * (position - lower)
        return {"mean": mean(values), "p10": percentile(.1), "p90": percentile(.9), "min": ordered[0], "max": ordered[-1], "stddev": pstdev(values), "valid_count": len(values)}
    return {"source_code": source_code, "unit": "p.u.", "grouping": "hour-of-day", "value_kind": "derived", "series": [{"hour": hour, **stats(values)} for hour, values in sorted(grouped.items())], "filters": {"month": month, "scenario": scenario}, "provenance": "derived from persisted renewable hourly input profiles"}


@router.get("/projects/{project_id}/assets/{asset_id}/profile-statistics", tags=["visualizer"])
def get_asset_profile_statistics(
    project_id: int,
    asset_id: int,
    month: int | None = None,
    scenario: int | None = None,
    tenant_id: int = Depends(tenant_from_header),
    db: Session = Depends(get_db),  # noqa: B008
):
    project = db.scalar(select(Project).where(Project.id == project_id, Project.tenant_id == tenant_id))
    if project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    revision = db.scalar(select(StudyRevision).where(StudyRevision.project_id == project_id, StudyRevision.is_active.is_(True)).order_by(StudyRevision.revision_number.desc()))
    asset = db.scalar(select(EnergyAsset).where(EnergyAsset.id == asset_id, EnergyAsset.revision_id == (revision.id if revision else -1)))
    if revision is None or asset is None:
        raise HTTPException(status_code=404, detail="Asset not found")
    job = db.scalar(select(StudyAnalyticsJob).where(StudyAnalyticsJob.revision_id == revision.id))
    if job and job.status in {"pending", "running"}:
        return {"asset_id": asset_id, "status": job.status, "progress": job.progress, "processed_assets": job.processed_assets, "total_assets": job.total_assets}
    if job and job.status == "failed":
        return {"asset_id": asset_id, "status": "failed", "error": job.error_message}
    kind = "hydro-monthly" if asset.asset_type == "hydro" else "renewable-daily"
    rows = list(db.scalars(select(StudyProfileStatistic).where(StudyProfileStatistic.revision_id == revision.id, StudyProfileStatistic.asset_id == asset.id, StudyProfileStatistic.profile_kind == kind).order_by(StudyProfileStatistic.bucket)))
    if not rows:
        message = "No hydro inflow series is linked to this generator." if kind == "hydro-monthly" else "No renewable profile series is linked to this generator."
        return {"asset_id": asset_id, "status": "not-applicable", "source_code": asset.source_code, "series": [], "message": message}
    series = []
    warnings = []
    for row in rows:
        warning = None
        if row.mean < row.p10 or row.mean > row.p90:
            warning = "Mean is outside the empirical P10-P90 range; inspect skew or outliers."
            if warning not in warnings:
                warnings.append(warning)
        series.append({
            "month" if kind == "hydro-monthly" else "hour": row.bucket,
            "mean": row.mean,
            "p10": row.p10,
            "p25": row.p25,
            "p75": row.p75,
            "p90": row.p90,
            "min": row.minimum,
            "max": row.maximum,
            "stddev": row.standard_deviation,
            "valid_count": row.valid_count,
            "warning": warning,
        })
    return {"asset_id": asset_id, "status": "ready", "source_code": asset.source_code, "unit": rows[0].unit_name, "grouping": rows[0].grouping, "statistics": _profile_stats([row.mean for row in rows]), "series": series, "warnings": warnings, "value_kind": "derived", "provenance": f"{rows[0].source_file or 'input series'} · precalculated for revision {revision.id}"}


@router.get("/projects/{project_id}/analytics/status", tags=["visualizer"])
def get_analytics_status(
    project_id: int,
    tenant_id: int = Depends(tenant_from_header),
    db: Session = Depends(get_db),  # noqa: B008
):
    project = db.scalar(select(Project).where(Project.id == project_id, Project.tenant_id == tenant_id))
    if project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    revision = db.scalar(select(StudyRevision).where(StudyRevision.project_id == project_id, StudyRevision.is_active.is_(True)).order_by(StudyRevision.revision_number.desc()))
    job = db.scalar(select(StudyAnalyticsJob).where(StudyAnalyticsJob.revision_id == (revision.id if revision else -1)))
    if job is None:
        return {"status": "not-started", "progress": 0, "processed_assets": 0, "total_assets": 0}
    return {"status": job.status, "phase": job.phase, "progress": job.progress, "processed_assets": job.processed_assets, "total_assets": job.total_assets, "error": job.error_message}


@router.get("/projects/{project_id}/hydro-inflows/{station_code}/statistics", tags=["visualizer"])
def get_hydro_inflow_statistics(
    project_id: int,
    station_code: str,
    db: Session = Depends(get_db),  # noqa: B008
    tenant_id: int = Depends(tenant_from_header),
):
    project = db.scalar(select(Project).where(Project.id == project_id, Project.tenant_id == tenant_id))
    if project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    revision = db.scalar(select(StudyRevision).where(StudyRevision.project_id == project_id, StudyRevision.is_active.is_(True)).order_by(StudyRevision.revision_number.desc()))
    if revision is None:
        raise HTTPException(status_code=404, detail="Active study revision not found")
    rows = list(db.scalars(select(StudyHydroInflow).where(StudyHydroInflow.revision_id == revision.id, StudyHydroInflow.station_code == station_code, StudyHydroInflow.is_missing.is_(False))))
    if not rows:
        raise HTTPException(status_code=404, detail="Hydro inflow input series not found")
    grouped: dict[int, list[float]] = {}
    for row in rows:
        if row.value_m3s is not None:
            grouped.setdefault(row.month, []).append(row.value_m3s)
    def stats(values: list[float]) -> dict[str, float | int]:
        ordered = sorted(values)
        def percentile(fraction: float) -> float:
            position = (len(ordered) - 1) * fraction
            lower = int(position)
            upper = min(lower + 1, len(ordered) - 1)
            return ordered[lower] + (ordered[upper] - ordered[lower]) * (position - lower)
        return {"mean": mean(values), "p10": percentile(.1), "p90": percentile(.9), "min": ordered[0], "max": ordered[-1], "stddev": pstdev(values), "valid_count": len(values)}
    missing_rows = list(db.scalars(select(StudyHydroInflow).where(StudyHydroInflow.revision_id == revision.id, StudyHydroInflow.station_code == station_code, StudyHydroInflow.is_missing.is_(True))))
    return {"station_code": station_code, "unit": "m3/s", "grouping": "month-of-year", "value_kind": "derived", "series": [{"month": month, **stats(values)} for month, values in sorted(grouped.items())], "missing_count": len(missing_rows), "provenance": "derived from persisted hydro input inflows"}
