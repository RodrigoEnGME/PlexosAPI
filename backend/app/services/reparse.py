"""Idempotent repairs for semantic data already persisted in a revision."""

from dataclasses import dataclass
from pathlib import Path

from sqlalchemy import delete
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.models import AssetModification, Project, StudyRevision
from app.services.intermediate_model import _load_modifications

MODIFICATION_TYPES = ("renewable", "thermal", "hydro", "circuit")


@dataclass(frozen=True)
class ReparseResult:
    revision_id: int
    project: str
    source_root: str | None
    status: str
    deleted: int = 0
    inserted: int = 0
    error: str | None = None


def resolve_revision_source(
    revision: StudyRevision,
    artifact_root: str | Path,
    fallback_roots: dict[str, str | Path] | None = None,
) -> Path | None:
    candidates: list[Path] = []
    if revision.import_run and revision.import_run.source_path:
        candidates.append(Path(revision.import_run.source_path))
    if revision.source_archive_uri:
        archive_path = Path(revision.source_archive_uri)
        candidates.extend((archive_path.parent / "source", archive_path.parent))
    project = revision.project
    root = Path(artifact_root)
    candidates.append(root / str(project.tenant_id) / str(project.id) / f"revision-{revision.revision_number}" / "source")
    if fallback_roots and project.name in fallback_roots:
        candidates.append(Path(fallback_roots[project.name]))
    return next((candidate for candidate in candidates if candidate.is_dir()), None)


def reparse_revision_modifications(
    revision: StudyRevision,
    db: Session,
    source_root: str | Path,
) -> ReparseResult:
    root = Path(source_root)
    if not root.is_dir():
        return ReparseResult(revision.id, revision.project.name, str(root), "skipped", error="source root does not exist")
    try:
        deleted = db.execute(
            delete(AssetModification).where(
                AssetModification.revision_id == revision.id,
                AssetModification.entity_type.in_(MODIFICATION_TYPES),
            )
        ).rowcount or 0
        db.flush()
        inserted = _load_modifications(root, revision, db)
        if deleted and not inserted:
            db.rollback()
            return ReparseResult(
                revision.id,
                revision.project.name,
                str(root),
                "failed",
                deleted=deleted,
                error="parser produced zero modifications; existing rows were preserved",
            )
        db.commit()
        return ReparseResult(revision.id, revision.project.name, str(root), "reparsed", deleted, inserted)
    except (OSError, SQLAlchemyError, ValueError) as exc:
        db.rollback()
        return ReparseResult(revision.id, revision.project.name, str(root), "failed", error=str(exc))


def reparse_all_revisions(
    db: Session,
    artifact_root: str | Path,
    fallback_roots: dict[str, str | Path] | None = None,
) -> list[ReparseResult]:
    revisions = db.query(StudyRevision).join(Project).order_by(StudyRevision.id).all()
    results: list[ReparseResult] = []
    for revision in revisions:
        active_fallback = fallback_roots.get(revision.project.name) if revision.is_active and fallback_roots else None
        source_root = Path(active_fallback) if active_fallback and Path(active_fallback).is_dir() else resolve_revision_source(revision, artifact_root, None)
        if source_root is None:
            results.append(ReparseResult(revision.id, revision.project.name, None, "skipped", error="source root not resolvable"))
            continue
        results.append(reparse_revision_modifications(revision, db, source_root))
    return results
