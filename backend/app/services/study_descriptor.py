import csv
import json
from pathlib import Path

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Project, StudyDescriptor
from app.services.dataset_parser import parse_sddp_control


def _parse_block_durations(root: Path, warnings: list[str]) -> dict[str, list[float]]:
    csv_path = next((path for path in root.rglob("duraci.csv") if path.is_file()), None)
    if csv_path is None:
        binary_path = next((path for path in root.rglob("duraci.bin") if path.is_file()), None)
        if binary_path:
            warnings.append(f"Block durations require a documented binary decoder: {binary_path.name}")
        return {}
    durations: dict[str, list[float]] = {}
    with csv_path.open("r", encoding="latin-1", errors="replace", newline="") as stream:
        for row in csv.reader(stream):
            if len(row) < 4 or not row[0].strip().isdigit():
                continue
            try:
                stage = int(row[0])
                block = int(row[2])
                hours = float(row[3].strip().replace(",", "."))
            except ValueError:
                continue
            values = durations.setdefault(str(stage), [])
            while len(values) < block:
                values.append(0.0)
            values[block - 1] = hours
    return durations


def build_study_descriptor(
    project: Project,
    dataset_root: str | Path,
    db: Session,
    revision_id: int | None = None,
) -> StudyDescriptor:
    root = Path(dataset_root)
    control = next((p for p in root.rglob("*") if p.is_file() and p.name.lower() == "sddp.dat"), None)
    if control is None:
        raise FileNotFoundError(f"No sddp.dat found in {root}")
    descriptor = parse_sddp_control(control)
    descriptor["block_durations_hours"] = _parse_block_durations(root, descriptor["warnings"])
    existing = db.scalar(select(StudyDescriptor).where(
        StudyDescriptor.project_id == project.id,
        StudyDescriptor.revision_id == revision_id,
    ))
    if existing is None:
        existing = StudyDescriptor(
            project_id=project.id,
            revision_id=revision_id,
            source_file=control.name,
            descriptor_json="{}",
        )
        db.add(existing)
    existing.source_file = control.relative_to(root).as_posix()
    existing.descriptor_json = json.dumps(descriptor, ensure_ascii=False)
    existing.warnings_json = json.dumps(descriptor.get("warnings", []), ensure_ascii=False)
    db.commit()
    db.refresh(existing)
    return existing
