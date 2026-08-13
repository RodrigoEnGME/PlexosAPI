import argparse

from app.db import SessionLocal, init_db
from app.models import ImportRun, Project, StudyRevision, Tenant
from app.services.dataset_parser import import_folder
from app.services.intermediate_model import build_intermediate_model
from app.services.study_descriptor import build_study_descriptor


def main() -> None:
    parser = argparse.ArgumentParser(description="Import and inventory an SDDP dataset folder")
    parser.add_argument("folder", help="Folder containing the SDDP dataset")
    parser.add_argument("--tenant", default="GME")
    parser.add_argument("--tenant-code", default="gme")
    parser.add_argument("--project", default="UY SDDP")
    args = parser.parse_args()
    init_db()
    db = SessionLocal()
    try:
        tenant = db.query(Tenant).filter(Tenant.code == args.tenant_code).first()
        if tenant is None:
            tenant = Tenant(name=args.tenant, code=args.tenant_code)
            db.add(tenant)
            db.flush()
        project = db.query(Project).filter(Project.tenant_id == tenant.id, Project.name == args.project).first()
        if project is None:
            project = Project(name=args.project, tenant_id=tenant.id)
            db.add(project)
            db.flush()
        run = ImportRun(project_id=project.id, source_path=args.folder)
        db.add(run)
        db.flush()
        print(import_folder(args.folder, project.id, db, run))
        descriptor = build_study_descriptor(project, args.folder, db)
        revision_number = (db.query(StudyRevision).filter(StudyRevision.project_id == project.id).count() + 1)
        revision = StudyRevision(
            project_id=project.id,
            import_run_id=run.id,
            revision_number=revision_number,
            status="parsing",
            is_active=True,
        )
        db.add(revision)
        db.flush()
        print(build_intermediate_model(args.folder, revision, db))
        print(descriptor.descriptor_json)
    finally:
        db.close()


if __name__ == "__main__":
    main()
