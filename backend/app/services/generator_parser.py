import re
from pathlib import Path

from pydantic import BaseModel


class GeneratorInput(BaseModel):
    id: str
    name: str
    technology: str
    bus: int
    capacity_mw: float
    operating_factor: float
    source_file: str
    source_line: int
    latitude: float | None = None
    longitude: float | None = None
    coordinate_status: str = "not-provided"


LINE_RE = re.compile(
    r"^\s*(?P<date>\d{2}/\d{2}/\d{4})\s+"
    r"(?P<bus>\d+)\s+"
    r"(?P<name>.{1,20}?)\s+"
    r"(?:(?P<plant_type>\d+)\s+)?(?P<units>\d+)\s+"
    r"(?P<capacity>[-+\d.Ee]+)\s+"
    r"(?P<factor>[-+\d.Ee]+)"
)


def _technology(name: str) -> str:
    normalized = name.upper()
    if "HID" in normalized or "SALTO" in normalized or "PALMAR" in normalized:
        return "hydro"
    if "EOL" in normalized or "WIND" in normalized:
        return "wind"
    if "SOL" in normalized or "PV" in normalized:
        return "solar"
    if "BIC" in normalized or "TERM" in normalized:
        return "thermal"
    return "generator"


def parse_mgnd(path: str | Path) -> list[GeneratorInput]:
    source = Path(path)
    generators: list[GeneratorInput] = []
    with source.open("r", encoding="latin-1", errors="replace") as stream:
        for line_number, line in enumerate(stream, start=1):
            match = LINE_RE.match(line.rstrip("\r\n"))
            if not match:
                continue
            values = match.groupdict()
            name = values["name"].strip().replace("_", " ")
            generators.append(
                GeneratorInput(
                    id=f"{source.stem}:{line_number}",
                    name=name,
                    technology=_technology(name),
                    bus=int(values["bus"]),
                    capacity_mw=float(values["capacity"]),
                    operating_factor=float(values["factor"]),
                    source_file=source.name,
                    source_line=line_number,
                )
            )
    return generators
