import json
import tempfile
from pathlib import Path

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
    Conversion,
    DatasetFile,
    ImportRun,
    Project,
    StudyDescriptor,
    StudyRevision,
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
)
from app.services.encoding import detect_encoding
from app.services.import_service import run_import_job
from app.services.snapshot import effective_snapshot
from app.settings import settings

router = APIRouter()


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
