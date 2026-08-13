"""Safe first-pass parser for complete SDDP dataset folders.

The parser preserves source lines and provenance. It deliberately does not guess
proprietary binary schemas from .hdr/.bin/.psr files.
"""

import csv
import hashlib
import json
import re
from dataclasses import dataclass
from pathlib import Path

from sqlalchemy.orm import Session

from app.models import DatasetFile, DatasetRecord, ImportRun
from app.services.encoding import detect_encoding

TEXT_EXTENSIONS = {".dat", ".csv", ".log", ".out", ".grf", ".all", ".ok", ".bak", ".txt"}
BINARY_EXTENSIONS = {".bin", ".psr", ".hdr"}
LARGE_SERIES_PREFIXES = ("hr", "rr", "rs", "rx", "dbf", "deme", "dur")


@dataclass
class FileParseResult:
    file: DatasetFile
    records: list[DatasetRecord]


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _sample_bytes(path: Path, size: int = 64 * 1024) -> bytes:
    with path.open("rb") as source:
        return source.read(size)


def _classify(path: Path, sample: bytes) -> str:
    if path.suffix.lower() in BINARY_EXTENSIONS or b"\x00" in sample:
        return "binary"
    if path.suffix.lower() == ".csv":
        return "csv"
    if path.suffix.lower() in TEXT_EXTENSIONS:
        return "text"
    return "text" if sample else "empty"


def _section(line: str, current: str | None) -> str | None:
    stripped = line.strip()
    if stripped.startswith(("****", "#")):
        return stripped[:160]
    if stripped.startswith("MOD:"):
        return stripped[:160]
    return current


def _tokens(line: str, file_kind: str) -> list[str]:
    if file_kind == "csv":
        try:
            return next(csv.reader([line], skipinitialspace=True))
        except csv.Error:
            return line.split()
    return line.split()


def parse_file(path: Path, root: Path, project_id: int, db: Session, revision_id: int | None = None) -> FileParseResult:
    sample = _sample_bytes(path)
    file_kind = _classify(path, sample)
    relative_path = path.relative_to(root).as_posix()
    existing = (
        db.query(DatasetFile)
        .filter(
            DatasetFile.project_id == project_id,
            DatasetFile.revision_id == revision_id,
            DatasetFile.relative_path == relative_path,
        )
        .first()
    )
    if existing:
        db.delete(existing)
        db.flush()

    detection = detect_encoding(sample) if file_kind != "binary" else None
    asset = DatasetFile(
        project_id=project_id,
        revision_id=revision_id,
        relative_path=relative_path,
        extension=path.suffix.lower(),
        size_bytes=path.stat().st_size,
        sha256=_sha256(path),
        file_kind=file_kind,
        encoding=detection.encoding if detection else None,
        parse_status="discovered" if file_kind == "binary" else "parsed",
    )
    db.add(asset)
    db.flush()
    if file_kind == "binary":
        return FileParseResult(asset, [])

    # Preserve the artifact and metadata, but do not duplicate millions of
    # hourly/chronology lines in DatasetRecord. Semantic family parsers own
    # these large files later in the pipeline.
    if path.stem.lower().startswith(LARGE_SERIES_PREFIXES) and path.stat().st_size > 1_000_000:
        asset.parse_status = "inventory_only"
        asset.parse_message = "Large series retained as artifact; semantic streaming parser pending."
        asset.line_count = sum(1 for _ in path.open("rb"))
        return FileParseResult(asset, [])

    records: list[DatasetRecord] = []
    current_section: str | None = None
    line_count = 0
    try:
        with path.open("r", encoding=asset.encoding or "utf-8", errors="replace") as source:
            for line_number, line in enumerate(source, start=1):
                line_count = line_number
                raw = line.rstrip("\r\n")
                if not raw.strip():
                    continue
                current_section = _section(raw, current_section)
                stripped = raw.lstrip()
                record_kind = "comment" if stripped.startswith(("$", "!", "#", "*")) else "data"
                records.append(
                    DatasetRecord(
                        file_id=asset.id,
                        line_number=line_number,
                        section=current_section,
                        raw_text=raw,
                        tokens_json=json.dumps(_tokens(raw, file_kind), ensure_ascii=False),
                        record_kind=record_kind,
                    )
                )
                if len(records) >= 1000:
                    db.add_all(records)
                    db.flush()
                    records.clear()
    except (UnicodeError, OSError) as exc:
        asset.parse_status = "error"
        asset.parse_message = str(exc)
    asset.line_count = line_count
    asset.record_count = db.query(DatasetRecord).filter(DatasetRecord.file_id == asset.id).count() + len(records)
    db.add_all(records)
    db.flush()
    return FileParseResult(asset, records)


def import_folder(
    folder: str | Path,
    project_id: int,
    db: Session,
    run: ImportRun | None = None,
    revision_id: int | None = None,
) -> dict[str, int]:
    root = Path(folder).resolve()
    if not root.is_dir():
        raise NotADirectoryError(root)
    files = [path for path in root.rglob("*") if path.is_file()]
    if run:
        run.files_total = len(files)
        run.source_path = str(root)
        db.flush()
    parsed = 0
    binary = 0
    errors = 0
    for path in sorted(files):
        try:
            result = parse_file(path, root, project_id, db, revision_id)
            parsed += 1
            binary += result.file.file_kind == "binary"
            errors += result.file.parse_status == "error"
            if run:
                run.files_processed = parsed
                run.files_binary = binary
                run.errors = errors
            if parsed % 25 == 0:
                db.commit()
        except OSError:
            errors += 1
    db.commit()
    result = {"files": parsed, "binary_files": binary, "errors": errors}
    if run:
        run.status = "completed" if errors == 0 else "completed_with_errors"
        run.message = json.dumps(result)
        db.commit()
    return result


CONTROL_KEY_RE = re.compile(r"^\s*([^\d\s][^\r\n]*?)\s{2,}(.+?)\s*$")


def parse_sddp_control(path: str | Path) -> dict[str, object]:
    """Parse the human-readable key/value control section of SDDP.DAT."""
    source = Path(path)
    raw = _sample_bytes(source, 2 * 1024 * 1024)
    detection = detect_encoding(raw)
    values: dict[str, object] = {"source_file": source.name, "encoding": detection.encoding}
    warnings: list[str] = []
    section_started = False
    with source.open("r", encoding=detection.encoding, errors="replace") as stream:
        for number, line in enumerate(stream, start=1):
            text = line.rstrip("\r\n")
            if text.lstrip().startswith("-") and "SISTEMAS" in text.upper():
                section_started = True
            if section_started or not text.strip() or text.startswith(("-", ".")):
                continue
            match = CONTROL_KEY_RE.match(text)
            if not match:
                continue
            key, raw_value = match.groups()
            key = re.sub(r"\s+", " ", key.strip()).lower()
            if key in values:
                continue
            numeric_tokens: list[str] = []
            for token in raw_value.split():
                if "=" in token:
                    break
                if not re.fullmatch(r"[-+]?(?:\d+(?:[.,]\d*)?|[.,]\d+)", token):
                    break
                numeric_tokens.append(token)
            if not numeric_tokens:
                values[key] = raw_value.strip()
                continue
            parsed_tokens: list[int | float] = []
            for token in numeric_tokens:
                normalized = token.replace(",", ".")
                parsed_tokens.append(float(normalized) if "." in normalized else int(normalized))
            values[key] = parsed_tokens[0] if len(parsed_tokens) == 1 else parsed_tokens
    values["warnings"] = warnings
    return values
