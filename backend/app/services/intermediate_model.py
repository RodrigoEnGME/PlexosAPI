"""Build the persisted intermediate model from one SDDP study directory."""

import csv
import json
import re
from datetime import UTC, datetime
from pathlib import Path

from sqlalchemy.orm import Session

from app.models import (
    AssetModification,
    EnergyAsset,
    StudyBus,
    StudyBusDemand,
    StudyCircuit,
    StudyDemand,
    StudyDescriptor,
    StudyMaintenance,
    StudyRevision,
    StudySystem,
)

DATE_RE = re.compile(r"MOD:\s*(\d{2})/(\d{2})/(\d{4})")
GEN_RE = re.compile(
    r"^\s*(?P<date>\d{2}/\d{2}/\d{4})\s+(?P<code>\d+)\s+(?P<name>.{1,20}?)\s+"
    r"(?P<plant_type>\d+)\s+(?P<units>\d+)\s+"
    r"(?P<capacity>[-+\d.Ee]+)\s+(?P<factor>[-+\d.Ee]+)"
)
THERMAL_RE = re.compile(r"^\s*(?P<code>\d+)\s+(?P<name>.{1,12}?)\s+(?P<units>\d+)\s+(?P<future>\d+)\s+(?P<capacity>[-+\d.Ee]+)")
RENEWABLE_RE = re.compile(r"^\s*(?P<code>\d+)\s+(?P<name>.{1,12}?)\s+(?P<bus>\d+)\s+(?P<future>\d+)\s+(?P<units>\d+)\s+(?P<capacity>[-+\d.Ee]+)")
VOLTAGE_RE = re.compile(r"(?:^|[^\d])(?P<voltage>500|230|138|115|69|44|22|13(?:\.8)?)\s*(?:KV|K)?(?:$|[^\d])", re.IGNORECASE)


def _number(value: str) -> float:
    return float(value.replace(",", "."))


def _optional_number(value: str) -> float | None:
    normalized = value.strip().replace(",", ".")
    if not normalized or normalized in {".", "-", "+"}:
        return None
    try:
        return float(normalized)
    except ValueError:
        return None


def _find(root: Path, name: str) -> Path | None:
    return next((path for path in root.rglob("*") if path.is_file() and path.name.lower() == name.lower()), None)


def _files(root: Path, pattern: str) -> list[Path]:
    """Discover the same family whether the source is flat or ZIP-nested."""
    return sorted(path for path in root.rglob(pattern) if path.is_file())


def _read_lines(path: Path) -> list[tuple[int, str]]:
    with path.open(encoding="latin-1", errors="replace") as stream:
        return [(number, line.rstrip("\r\n")) for number, line in enumerate(stream, 1)]


def _voltage_from_name(name: str) -> float | None:
    match = VOLTAGE_RE.search(name)
    return float(match.group("voltage")) if match else None


def _load_systems(root: Path, revision: StudyRevision, db: Session) -> dict[str, StudySystem]:
    path = _find(root, "sistem.dat")
    systems: dict[str, StudySystem] = {}
    if path:
        for _, line in _read_lines(path):
            fields = line.split()
            if len(fields) < 4 or not fields[0].isdigit():
                continue
            code, suffix, _unit = fields[0], fields[-2], fields[-1]
            name = " ".join(fields[1:-2])
            if len(suffix) != 2:
                continue
            system = StudySystem(revision_id=revision.id, code=code, name=name.strip(), country_code=suffix.lower())
            db.add(system)
            systems[suffix.lower()] = system
    if not systems:
        system = StudySystem(revision_id=revision.id, code="1", name="Unknown system", country_code=None)
        db.add(system)
        systems[""] = system
    db.flush()
    return systems


def _load_buses(root: Path, revision: StudyRevision, systems: dict[str, StudySystem], db: Session) -> dict[str, StudyBus]:
    path = _find(root, "dbus.dat")
    result: dict[str, StudyBus] = {}
    if path is None:
        return result
    coordinates: dict[str, tuple[float, float, str]] = {}
    coord_path = _find(root, "dgbus.dat")
    if coord_path:
        for line_number, line in _read_lines(coord_path):
            match = re.match(r"^\s*(\d+)\s+([-+\d.]+)\s+([-+\d.]+)", line)
            if match:
                code, lat, lon = match.groups()
                coordinates[code] = (float(lat), float(lon), f"{coord_path.name}:{line_number}")
    for line_number, line in _read_lines(path):
        code = line[:5].strip()
        if not code.isdigit() or code in result:
            continue
        name = line[9:21].strip() or code
        suffix = line[22:24].strip().lower()
        system = systems.get(suffix) or systems.get("")
        coordinate = coordinates.get(code)
        demand = {str(index + 1): _optional_number(line[60 + index * 20:65 + index * 20]) for index in range(5)}
        bus = StudyBus(
            revision_id=revision.id,
            source_code=code,
            name=name,
            system_id=system.id if system else None,
            latitude=coordinate[0] if coordinate else None,
            longitude=coordinate[1] if coordinate else None,
            coordinate_source=coordinate[2] if coordinate else None,
            nominal_voltage_kv=_voltage_from_name(name),
            demand_block_mw_json=json.dumps({key: value for key, value in demand.items() if value is not None}),
            source_file=path.name, source_line=line_number,
        )
        db.add(bus)
        result[code] = bus
    db.flush()
    return result


def _load_asset_buses(root: Path) -> dict[str, str]:
    path = _find(root, "dbus.dat")
    result: dict[tuple[str, str, str], str] = {}
    if path is None:
        return result
    for _, line in _read_lines(path):
        if not line[:5].strip().isdigit():
            continue
        bus, suffix = line[:5].strip(), line[22:24].strip().lower()
        plant_type, code = line[29:30].strip(), line[31:35].strip()
        if plant_type in {"1", "2"} and code.isdigit():
            result[(suffix, plant_type, code)] = bus
    return result


def _load_base_assets(root: Path, revision: StudyRevision, systems: dict[str, StudySystem], db: Session) -> int:
    count = 0
    asset_buses = _load_asset_buses(root)
    for prefix, asset_type, pattern in (("ctermi", "thermal", THERMAL_RE), ("cgnd", "renewable", RENEWABLE_RE)):
        for path in _files(root, f"{prefix}*.dat"):
            suffix = path.stem[len(prefix):].lower()
            system = systems.get(suffix) or systems.get("")
            for line_number, line in _read_lines(path):
                match = pattern.match(line)
                if not match:
                    continue
                values = match.groupdict()
                plant_type = "2" if asset_type == "thermal" else "1"
                bus = values.get("bus") or asset_buses.get((suffix, plant_type, values["code"]))
                db.add(EnergyAsset(
                revision_id=revision.id,
                system_id=system.id if system else None,
                bus_code=bus,
                source_code=values["code"],
                name=values["name"].strip().replace("_", " "),
                asset_type=asset_type,
                technology=values["name"].strip().split("_")[-1],
                capacity_mw=_number(values["capacity"]),
                lifecycle_status="future" if values.get("future") == "1" else "existing",
                    source_file=path.name,
                    source_line=line_number,
                ))
                count += 1
    for path in _files(root, "chidro*.dat"):
        suffix = path.stem[6:].lower()
        system = systems.get(suffix) or systems.get("")
        for line_number, line in _read_lines(path):
            match = re.match(r"^\s*(\d+)\s+(.{1,12}?)\s+.*?\s+(\d+)\s+\d+\s+([-+\d.Ee]+)", line)
            if match:
                code, name, _units, capacity = match.groups()
                db.add(EnergyAsset(
                    revision_id=revision.id, system_id=system.id if system else None, bus_code=asset_buses.get((suffix, "1", code)), source_code=code,
                    name=name.strip(), asset_type="hydro", technology="hydro",
                    capacity_mw=_number(capacity), lifecycle_status="existing",
                    source_file=path.name, source_line=line_number,
                ))
                count += 1
    db.flush()
    return count


def _load_circuits(root: Path, revision: StudyRevision, db: Session) -> int:
    path = _find(root, "atcirc.csv") or _find(root, "dcirc.dat")
    if path is None:
        return 0
    count = 0
    if path.suffix.lower() == ".csv":
        with path.open(encoding="latin-1", errors="replace", newline="") as stream:
            rows = list(csv.reader(stream))
        if len(rows) < 3:
            return 0
        headers = [value.strip().lower() for value in rows[0]]
        for line_number, row in enumerate(rows[2:], start=3):
            if not row or len(row) <= 12:
                continue
            values = {headers[index]: value.strip() for index, value in enumerate(row) if index < len(headers)}
            code = values.get("codigo")
            if not code or not values.get("# barra de") or not values.get("# barra para"):
                continue
            db.add(StudyCircuit(
                revision_id=revision.id,
                source_code=code,
                from_bus=values["# barra de"],
                to_bus=values["# barra para"],
                name=values.get("nombre", code),
                normal_limit_mw=_number(values["capacidad"]) if values.get("capacidad") else None,
                emergency_limit_mw=_number(values["cap. emerg."]) if values.get("cap. emerg.") else None,
                status="connected" if values.get("existente", "1") == "1" else "future",
            ))
            count += 1
    else:
        for line_number, line in _read_lines(path):
            if not line[:5].strip().isdigit() or not line[8:13].strip().isdigit():
                continue
            from_bus, to_bus = line[:5].strip(), line[8:13].strip()
            source_code = line[69:74].strip() or f"{from_bus}-{to_bus}-{line_number}"
            normal = line[58:64].strip()
            emergency = line[64:68].strip()
            plant_type = line[75:76].strip()
            status = line[127:128].strip()
            db.add(StudyCircuit(
                revision_id=revision.id, source_code=source_code, from_bus=from_bus, to_bus=to_bus,
                name=line[30:42].strip() or f"CIRC-{source_code}",
                normal_limit_mw=_optional_number(normal),
                emergency_limit_mw=_optional_number(emergency),
                status=("future-disconnected" if plant_type == "1" and status == "1" else "future" if plant_type == "1" else "disconnected" if status == "1" else "connected"),
                nominal_voltage_kv=_voltage_from_name(line[30:42]), voltage_source="inferred:circuit-name" if _voltage_from_name(line[30:42]) else None,
                source_file=path.name, source_line=line_number,
            ))
            count += 1
    db.flush()
    return count


def _load_modifications(root: Path, revision: StudyRevision, db: Session) -> int:
    count = 0
    for prefix, entity_type in (("mgnd", "renewable"), ("mtermi", "thermal"), ("mhidro", "hydro"), ("mcirc", "circuit")):
      for path in _files(root, f"{prefix}*.dat"):
        effective: datetime | None = None
        sequence = 0
        for line_number, line in _read_lines(path):
            date_match = DATE_RE.search(line)
            if date_match:
                day, month, year = date_match.groups()
                effective = datetime(int(year), int(month), int(day), tzinfo=UTC)
                continue
            if not line.strip() or line.lstrip().startswith(("$", "!", "#", "*")):
                continue
            values: dict[str, object] = {"raw": line}
            if entity_type == "renewable":
                match = GEN_RE.match(line)
                if not match:
                    continue
                values = match.groupdict()
                source_code = values["code"]
                day, month, year = values["date"].split("/")
                effective = datetime(int(year), int(month), int(day), tzinfo=UTC)
            elif entity_type in {"thermal", "hydro"}:
                match = re.match(
                    r"^\s*(\d+)\s+(.{1,12}?)\s+\d+\s+\d+\s+"
                    r"(?P<capacity>[-+\d.Ee]+)\s+[-+\d.Ee]+\s+[-+\d.Ee]+\s+"
                    r"(?P<teif>[-+\d.Ee]+)\s+(?P<ih>[-+\d.Ee]+)\s+(?P<variable_cost>[-+\d.Ee]+)",
                    line,
                )
                if not match:
                    continue
                source_code, name = match.group(1), match.group(2)
                values = {
                    "name": name.strip(),
                    "capacity": match.group("capacity"),
                    "teif": match.group("teif"),
                    "ih": match.group("ih"),
                    "variable_cost": match.group("variable_cost"),
                }
            else:
                fields = line.split()
                if len(fields) < 3:
                    continue
                source_code = fields[-1]
                values = {"from_bus": fields[0], "to_bus": fields[1], "raw_fields": fields[2:]}
            db.add(AssetModification(
                revision_id=revision.id, entity_type=entity_type, source_code=source_code,
                effective_date=effective, changed_fields_json=json.dumps(values, ensure_ascii=False),
                source_file=path.name, source_line=line_number, sequence=sequence,
            ))
            sequence += 1
            count += 1
    db.flush()
    return count


def _load_maintenance(root: Path, revision: StudyRevision, db: Session) -> int:
    """Parse PMHI/PMTR fixed-layout maintenance files without losing source rows."""
    count = 0
    for path in sorted(root.rglob("pm*.dat")):
        name = path.name.lower()
        if not name.startswith(("pmhi", "pmtr")):
            continue
        asset_type = "hydro" if name.startswith("pmhi") else "thermal"
        measure_type: int | None = None
        unit_type: int | None = None
        source_code: str | None = None
        asset_name = ""
        for line_number, line in _read_lines(path):
            info = re.search(r"Tipo Info\.\s*:\s*(\d+)", line, re.IGNORECASE)
            if info:
                measure_type = int(info.group(1))
                continue
            units = re.search(r"Unidades\s*:\s*(\d+)", line, re.IGNORECASE)
            if units:
                unit_type = int(units.group(1))
                continue
            plant = re.match(r"^\*\*\*\*\s*Planta:\s*(\d+)\s*(.*)$", line, re.IGNORECASE)
            if plant:
                source_code, asset_name = plant.group(1), plant.group(2).strip()
                continue
            values = line.split()
            if not values or not values[0].isdigit() or source_code is None:
                continue
            year = int(values[0])
            stage_values = [_number(value) for value in values[1:]]
            warnings: list[str] = []
            if measure_type is None or unit_type is None:
                warnings.append("missing maintenance type or units header")
            if not stage_values:
                warnings.append("maintenance row has no stage values")
            db.add(StudyMaintenance(
                revision_id=revision.id,
                asset_type=asset_type,
                source_code=source_code,
                asset_name=asset_name,
                measure_type=measure_type or 0,
                unit_type=unit_type or 0,
                year=year,
                stage_values_json=json.dumps(stage_values),
                source_file=path.name,
                source_line=line_number,
                warnings_json=json.dumps(warnings),
            ))
            count += 1
    db.flush()
    return count


def _load_demands(root: Path, revision: StudyRevision, systems: dict[str, StudySystem], db: Session) -> int:
    count = 0
    for path in _files(root, "deme*.dat"):
        suffix_match = re.search(r"deme\d+[a-z]+$", path.stem.lower())
        suffix = re.sub(r"^deme\d+", "", suffix_match.group()) if suffix_match else path.stem[4:].lower()
        system = systems.get(suffix) or systems.get("")
        current_code: str | None = None
        current_segment = 1
        for line_number, line in _read_lines(path):
            header = re.match(r"^\*\*\*\*\s*Load:\s*(\d+)\s+.*?Sgmnt:\s*(\d+)", line, re.IGNORECASE)
            if header:
                current_code, current_segment = header.groups()
                continue
            if current_code is None or not line[:4].strip().isdigit():
                continue
            values = line.split()
            if len(values) < 3:
                continue
            try:
                year, block = int(values[0]), int(values[1])
                monthly = [float(value.replace(",", ".")) for value in values[2:14]]
            except ValueError:
                continue
            db.add(StudyDemand(revision_id=revision.id, system_id=system.id if system else None, source_code=current_code, segment=int(current_segment), year=year, block=block, monthly_gwh_json=json.dumps(monthly), source_file=path.name, source_line=line_number))
            count += 1
    db.flush()
    return count


def _load_batteries(root: Path, revision: StudyRevision, systems: dict[str, StudySystem], db: Session) -> tuple[int, int]:
    assets = modifications = 0
    for path in _files(root, "cbattery*.dat"):
        suffix = path.stem[len("cbattery"):].lower()
        system = systems.get(suffix) or systems.get("")
        with path.open(encoding="latin-1", errors="replace", newline="") as stream:
            for line_number, row in enumerate(csv.reader(stream), start=1):
                if len(row) < 8 or not row[0].strip().isdigit() or row[0].strip().startswith("$"):
                    continue
                values = [value.strip() for value in row]
                try:
                    code, name, bus, future = values[0], values[1], values[2], values[3]
                    capacity = _number(values[7])
                except (IndexError, ValueError):
                    continue
                db.add(EnergyAsset(
                    revision_id=revision.id, system_id=system.id if system else None,
                    bus_code=bus if bus.isdigit() else None, source_code=code,
                    name=name, asset_type="battery", technology="battery",
                    capacity_mw=capacity, lifecycle_status="future" if future == "1" else "existing",
                    source_file=path.name, source_line=line_number,
                ))
                assets += 1
    for path in _files(root, "mbattery*.dat"):
        suffix = path.stem[len("mbattery"):].lower()
        for line_number, row in enumerate(csv.reader(path.open(encoding="latin-1", errors="replace", newline="")), start=1):
            values = [value.strip() for value in row]
            if len(values) < 7 or not values[0].isdigit() or not values[3].isdigit():
                continue
            year, month, day, code = map(int, values[:4])
            system = systems.get(suffix) or systems.get("")
            changed = {}
            if values[5].isdigit():
                changed["bus"] = values[5]
            if values[6] in {"0", "1"}:
                changed["existing"] = values[6]
            if len(values) > 10 and values[10]:
                changed["capacity"] = values[10]
            if not changed:
                continue
            db.add(AssetModification(
                revision_id=revision.id, entity_type="battery", source_code=code,
                effective_date=datetime(year, month, day, tzinfo=UTC), effective_stage=None,
                effective_block=None, changed_fields_json=json.dumps(changed),
                source_file=path.name, source_line=line_number, sequence=0,
            ))
            modifications += 1
    db.flush()
    return assets, modifications


def _load_bus_demands(root: Path, revision: StudyRevision, db: Session) -> int:
    count = 0
    for path in _files(root, "dbf*.dat"):
        for line_number, line in _read_lines(path):
            if not line[:5].strip().isdigit() or not line[35:39].strip().isdigit():
                continue
            try:
                bus_code = line[:5].strip()
                demand_code = line[19:23].strip()
                day, month, year = (int(value) for value in re.split(r"/", line[24:34].strip()))
                block = int(line[35:39].strip())
                demand_mw = float(line[40:48].strip().replace(",", "."))
            except (ValueError, IndexError):
                continue
            db.add(StudyBusDemand(revision_id=revision.id, bus_code=bus_code, demand_code=demand_code, effective_date=datetime(year, month, day, tzinfo=UTC), block=block, demand_mw=demand_mw, source_file=path.name, source_line=line_number))
            count += 1
    db.flush()
    return count


def build_intermediate_model(root: str | Path, revision: StudyRevision, db: Session) -> dict[str, int]:
    root_path = Path(root)
    systems = _load_systems(root_path, revision, db)
    buses = _load_buses(root_path, revision, systems, db)
    assets = _load_base_assets(root_path, revision, systems, db)
    circuits = _load_circuits(root_path, revision, db)
    modifications = _load_modifications(root_path, revision, db)
    maintenance = _load_maintenance(root_path, revision, db)
    demands = _load_demands(root_path, revision, systems, db)
    batteries, battery_modifications = _load_batteries(root_path, revision, systems, db)
    bus_demands = _load_bus_demands(root_path, revision, db)
    descriptor = db.query(StudyDescriptor).filter_by(revision_id=revision.id).first()
    if descriptor:
        warnings = json.loads(descriptor.warnings_json or "[]")
        unsupported = {
            "htopol.dat": "Hydrological topology is inventoried but not semantically decoded.",
            "hinflw.dat": "Natural inflow series is inventoried but not semantically decoded.",
            "csumcirc.dat": "Summed-circuit restrictions are inventoried but not semantically decoded.",
            "msumcirc021.dat": "Dated summed-circuit restrictions are inventoried but not semantically decoded.",
            "ccirme21.dat": "Directional circuit costs are inventoried but not semantically decoded.",
            "genctr.dat": "Generic constraints are inventoried but not semantically decoded.",
        }
        for filename, message in unsupported.items():
            if _find(root_path, filename) and message not in warnings:
                warnings.append(message)
        descriptor.warnings_json = json.dumps(warnings, ensure_ascii=False)
        db.flush()
    revision.status = "parsed"
    db.commit()
    return {"systems": len(systems), "buses": len(buses), "assets": assets, "circuits": circuits,
            "modifications": modifications + battery_modifications, "maintenance": maintenance, "demands": demands, "bus_demands": bus_demands, "batteries": batteries}
