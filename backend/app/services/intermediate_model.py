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
    StudyCurrency,
    StudyDemand,
    StudyDemandDefinition,
    StudyDescriptor,
    StudyFuel,
    StudyFuelPrice,
    StudyHourlyLoad,
    StudyHydroDetail,
    StudyHydroInflow,
    StudyHydroStation,
    StudyLoadLevelMap,
    StudyMaintenance,
    StudyRenewableAssignment,
    StudyRenewableDetail,
    StudyRenewableHourlyProfile,
    StudyRenewableProfile,
    StudyRevision,
    StudySystem,
    StudyThermalDetail,
)
from app.services.dataset_parser import parse_sddp_control
from app.services.language_profile import localized_marker_pattern

DATE_RE = re.compile(r"MOD:\s*(\d{2})/(\d{2})/(\d{4})")
GEN_RE = re.compile(
    r"^\s*(?P<date>\d{2}/\d{2}/\d{4})\s+(?P<code>\d+)\s+(?P<name>.{1,20}?)\s+"
    r"(?:(?P<plant_type>\d+)\s+)?(?P<units>\d+)\s+"
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


def _fixed_number(line: str, start: int, end: int) -> float | None:
    return _optional_number(line[start - 1:end])


def _fixed_int(line: str, start: int, end: int) -> int | None:
    value = line[start - 1:end].strip()
    try:
        return int(value) if value else None
    except ValueError:
        return None


def _curve_pairs(line: str, first_start: int, step: int, count: int) -> list[dict[str, float]]:
    result = []
    for index in range(count):
        value = _fixed_number(line, first_start + index * step, first_start + index * step + 6)
        x_value = _fixed_number(line, first_start + 8 + index * step, first_start + 14 + index * step)
        if value is not None and x_value is not None:
            result.append({"value": value, "x": x_value})
    return result


def _find(root: Path, name: str) -> Path | None:
    return next((path for path in root.rglob("*") if path.is_file() and path.name.lower() == name.lower()), None)


def _files(root: Path, pattern: str) -> list[Path]:
    """Discover the same family whether the source is flat or ZIP-nested."""
    return sorted(path for path in root.rglob(pattern) if path.is_file())


def _study_language_code(root: Path) -> int:
    control = _find(root, "sddp.dat")
    if control is None:
        return 1
    value = parse_sddp_control(control).get("idioma", 1)
    return int(value) if isinstance(value, (int, float)) else 1


def _canonical_family_files(root: Path, pattern: str) -> list[Path]:
    paths = _files(root, pattern)
    canonical = [path for path in paths if "_" not in path.stem]
    prefix = pattern.split("*")[0].lower()
    system_specific = [path for path in canonical if len(path.stem) == len(prefix) + 2 and path.stem.lower().startswith(prefix)]
    if system_specific:
        return system_specific
    base = [path for path in canonical if path.stem.lower() == prefix]
    return base or canonical or paths


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


def _load_generator_details(root: Path, revision: StudyRevision, db: Session) -> dict[str, int]:
    thermal = hydro = renewable = 0
    for path in _canonical_family_files(root, "ctermi*.dat"):
        for line_number, line in _read_lines(path):
            if not line[:4].strip().isdigit() or len(line) < 133:
                continue
            alternative_fuels = [_fixed_int(line, start, start + 3) for start in (140, 145, 150)]
            alternative_fuels = [value for value in alternative_fuels if value is not None and value > 0]
            segments = []
            for share_start, consumption_start in ((87, 95), (103, 111), (119, 127)):
                share = _fixed_number(line, share_start, share_start + 6)
                consumption = _fixed_number(line, consumption_start, consumption_start + 6)
                if share is not None or consumption is not None:
                    segments.append({"share_pct": share, "consumption_units_per_mwh": consumption})
            db.add(StudyThermalDetail(
                revision_id=revision.id, source_code=line[:4].strip(),
                unit_count=_fixed_int(line, 19, 22), plant_type=_fixed_int(line, 24, 27),
                min_generation_mw=_fixed_number(line, 37, 43), max_generation_mw=_fixed_number(line, 45, 51),
                short_term_outage_pct=_fixed_number(line, 53, 59), historical_outage_pct=_fixed_number(line, 61, 67),
                variable_om_cost=_fixed_number(line, 69, 75), fuel_code=str(_fixed_int(line, 82, 85) or "") or None,
                consumption_segments_json=json.dumps(segments), alternative_fuels_json=json.dumps(alternative_fuels),
                commitment_type=_fixed_int(line, 155, 158), transport_cost=_fixed_number(line, 160, 166),
                startup_cost=_fixed_number(line, 168, 174), gas_system=_fixed_int(line, 181, 184),
                combined_cycle_code=_fixed_int(line, 186, 189), emission_factor=_fixed_number(line, 204, 209),
                source_file=path.name, source_line=line_number,
            ))
            thermal += 1
    for path in _canonical_family_files(root, "cgnd*.dat"):
        for line_number, line in _read_lines(path):
            if not line[:4].strip().isdigit() or len(line) < 67:
                continue
            db.add(StudyRenewableDetail(
                revision_id=revision.id, source_code=line[0:4].strip(), unit_count=_fixed_int(line, 30, 33),
                plant_type=_fixed_int(line, 25, 28), operating_factor=_fixed_number(line, 43, 50),
                failure_probability=_fixed_number(line, 52, 58), technology_type=None,
                source_file=path.name, source_line=line_number,
            ))
            renewable += 1
    for path in _canonical_family_files(root, "chidro*.dat"):
        for line_number, line in _read_lines(path):
            if not line[:4].strip().isdigit() or len(line) < 130:
                continue
            production_curve = _curve_pairs(line, 132, 16, 5)
            level_curve = _curve_pairs(line, 372, 16, 5)
            db.add(StudyHydroDetail(
                revision_id=revision.id, source_code=line[0:4].strip(), station_code=_fixed_int(line, 19, 22),
                downstream_spill_code=_fixed_int(line, 24, 27), downstream_turbine_code=_fixed_int(line, 29, 32),
                unit_count=_fixed_int(line, 34, 37), plant_type=_fixed_int(line, 39, 42),
                production_factor=_fixed_number(line, 52, 58), min_turbine_flow=_fixed_number(line, 60, 66),
                max_turbine_flow=_fixed_number(line, 68, 74), min_volume_hm3=_fixed_number(line, 76, 82),
                max_volume_hm3=_fixed_number(line, 84, 90), initial_condition=_fixed_number(line, 92, 98),
                min_total_flow=_fixed_number(line, 100, 106), spill_mode=_fixed_int(line, 111, 114),
                short_term_outage_pct=_fixed_number(line, 116, 122), historical_outage_pct=_fixed_number(line, 124, 130),
                production_curve_json=json.dumps(production_curve), level_volume_curve_json=json.dumps(level_curve),
                source_file=path.name, source_line=line_number,
            ))
            hydro += 1
    db.flush()
    return {"thermal_details": thermal, "hydro_details": hydro, "renewable_details": renewable}


def _load_renewable_profiles(root: Path, revision: StudyRevision, db: Session) -> int:
    count = 0
    hourly_batch: list[dict[str, object]] = []
    profile_batch: list[dict[str, object]] = []
    for path in _files(root, "hrrenw*.dat"):
        headers: list[str] = []
        for line_number, line in _read_lines(path):
            if line.startswith("!") and "," in line:
                headers = [item.strip() for item in line[1:].split(",")][4:]
                continue
            fields = [item.strip() for item in line.split(",")]
            if not headers or len(fields) < 5:
                continue
            try:
                scenario, year, month, hour = map(int, fields[:4])
            except ValueError:
                continue
            for source_code, raw in zip(headers, fields[4:]):
                try:
                    value = float(raw.replace(",", "."))
                except ValueError:
                    continue
                hourly_batch.append({"revision_id": revision.id, "source_code": source_code, "scenario": scenario, "year": year, "month": month, "hour": hour, "value_pu": value, "source_file": path.name, "source_line": line_number})
                count += 1
                if len(hourly_batch) >= 50000:
                    db.bulk_insert_mappings(StudyRenewableHourlyProfile, hourly_batch)
                    hourly_batch.clear()
    for path in _files(root, "gnd*.dat"):
        if path.stem.lower().startswith(("gndsite", "gndbus")):
            continue
        headers: list[str] = []
        for line_number, line in _read_lines(path):
            fields = line.split()
            if len(fields) >= 4 and fields[0].lower().startswith("!stg"):
                headers = fields[3:]
                continue
            if not headers or len(fields) < 4:
                continue
            try:
                stage, scenario, block = map(int, fields[:3])
            except ValueError:
                continue
            for source_code, raw in zip(headers, fields[3:]):
                try:
                    value = float(raw.replace(",", "."))
                except ValueError:
                    continue
                profile_batch.append({"revision_id": revision.id, "source_code": source_code, "stage": stage, "scenario": scenario, "block": block, "value_pu": value, "source_file": path.name, "source_line": line_number})
                count += 1
                if len(profile_batch) >= 50000:
                    db.bulk_insert_mappings(StudyRenewableProfile, profile_batch)
                    profile_batch.clear()
    if hourly_batch:
        db.bulk_insert_mappings(StudyRenewableHourlyProfile, hourly_batch)
    if profile_batch:
        db.bulk_insert_mappings(StudyRenewableProfile, profile_batch)
    db.flush()
    return count


def _load_hourly_demand_inputs(root: Path, revision: StudyRevision, db: Session) -> dict[str, int]:
    """Persist HRBMAP and HRLOAD so DBF block weights can become hourly nodal load.

    HRBMAP maps month/hour to Llev. HRLOAD contains the aggregate system load
    and, when configured, direct elastic load columns. The nodal allocation
    itself remains a derived API value and is never stored as source input.
    """
    map_count = load_count = 0
    map_paths = _files(root, "hrbmap*.csv") or _files(root, "hrbmap*.dat")
    map_batch: list[dict[str, object]] = []
    for path in map_paths:
        for line_number, line in _read_lines(path):
            fields = [value.strip().replace(",", "") for value in line.split(",")]
            if len(fields) < 4 or not fields[0].lstrip("!").isdigit():
                continue
            try:
                year, month, hour, load_level = map(int, fields[:4])
            except ValueError:
                continue
            map_batch.append({"revision_id": revision.id, "year": year, "month": month, "hour": hour, "load_level": load_level, "source_file": path.name, "source_line": line_number})
            map_count += 1
            if len(map_batch) >= 50000:
                db.bulk_insert_mappings(StudyLoadLevelMap, map_batch)
                map_batch.clear()
    if map_batch:
        db.bulk_insert_mappings(StudyLoadLevelMap, map_batch)

    load_batch: list[dict[str, object]] = []
    for path in _files(root, "hrload*.dat"):
        headers: list[str] = []
        for line_number, line in _read_lines(path):
            if line.startswith("!") and "," in line:
                headers = [value.strip().lstrip("!") for value in line.split(",")]
                continue
            fields = [value.strip() for value in line.split(",")]
            if len(fields) < 4 or not headers:
                continue
            try:
                year, month, hour = map(int, fields[:3])
            except ValueError:
                continue
            for load_code, raw in zip(headers[3:], fields[3:]):
                if not load_code:
                    continue
                try:
                    value = float(raw.replace(",", "."))
                except ValueError:
                    continue
                load_batch.append({"revision_id": revision.id, "load_code": load_code, "year": year, "month": month, "hour": hour, "value_mw": value, "source_file": path.name, "source_line": line_number})
                load_count += 1
                if len(load_batch) >= 50000:
                    db.bulk_insert_mappings(StudyHourlyLoad, load_batch)
                    load_batch.clear()
    if load_batch:
        db.bulk_insert_mappings(StudyHourlyLoad, load_batch)
    db.flush()
    return {"load_level_maps": map_count, "hourly_loads": load_count}


def _load_renewable_assignments(root: Path, revision: StudyRevision, systems: dict[str, StudySystem], db: Session) -> int:
    count = 0
    assets = list(db.query(EnergyAsset).filter_by(revision_id=revision.id, asset_type="renewable"))
    by_key = {(asset.system_id, asset.source_code): asset for asset in assets}
    for path in _files(root, "gndsite*.dat"):
        suffix = path.stem[len("gndsite"):].lower()
        system = systems.get(suffix) or systems.get("")
        for line_number, line in _read_lines(path):
            if not line[:1].isdigit() or "," not in line:
                continue
            fields = [field.strip() for field in line.split(",")]
            if len(fields) < 4:
                continue
            site_code, profile_code, technology = fields[:3]
            asset = by_key.get((system.id if system else None, site_code))
            if asset is None:
                asset = next((item for item in assets if item.system_id == (system.id if system else None) and item.name.replace(" ", "_") == profile_code), None)
            if asset is None:
                continue
            try:
                technology_type = int(technology)
            except ValueError:
                technology_type = None
            db.add(StudyRenewableAssignment(revision_id=revision.id, asset_id=asset.id, site_code=site_code, profile_code=profile_code, technology_type=technology_type, source_file=path.name, source_line=line_number))
            count += 1
    db.flush()
    return count


def _load_hydro_inputs(root: Path, revision: StudyRevision, db: Session) -> dict[str, int]:
    stations = inflows = 0
    station_path = _find(root, "htopol.dat")
    station_codes: list[str] = []
    if station_path:
        for line_number, line in _read_lines(station_path):
            code = line[12:15].strip()
            if not code.isdigit():
                continue
            station_codes.append(code)
            db.add(StudyHydroStation(revision_id=revision.id, source_code=code, name=line[20:35].strip(), downstream_code=line[52:55].strip() or None, incremental_null=line[55:56].strip() == "*", source_file=station_path.name, source_line=line_number))
            stations += 1
    inflow_path = _find(root, "hinflw.dat")
    if inflow_path:
        headers: list[str] = []
        for line_number, line in _read_lines(inflow_path):
            if not headers:
                headers = [line[index:index + 7].strip() for index in range(7, len(line), 7)]
                headers = [code for code in headers if code]
                continue
            month = _fixed_int(line, 1, 2)
            year = _fixed_int(line, 4, 7)
            if month is None or year is None:
                continue
            for index, station_code in enumerate(headers):
                raw = line[7 + index * 7:14 + index * 7].strip()
                value = _optional_number(raw)
                db.add(StudyHydroInflow(revision_id=revision.id, station_code=station_code, month=month, year=year, value_m3s=None if value == -99 else value, is_missing=value == -99 or value is None, source_file=inflow_path.name, source_line=line_number))
                inflows += 1
    db.flush()
    return {"hydro_stations": stations, "hydro_inflows": inflows}


def _load_base_assets(root: Path, revision: StudyRevision, systems: dict[str, StudySystem], db: Session) -> int:
    count = 0
    asset_buses = _load_asset_buses(root)
    for prefix, asset_type, pattern in (("ctermi", "thermal", THERMAL_RE), ("cgnd", "renewable", RENEWABLE_RE)):
        for path in _canonical_family_files(root, f"{prefix}*.dat"):
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
    for path in _canonical_family_files(root, "chidro*.dat"):
        suffix = path.stem[6:].lower()
        system = systems.get(suffix) or systems.get("")
        for line_number, line in _read_lines(path):
            match = re.match(r"^\s*(\d+)\s+(.{1,12}?)\s+", line)
            if match:
                code, name = match.groups()
                # CHIDRO's Pot. field is fixed at columns 45-51; the
                # preceding numeric field is unit count, not MW capacity.
                capacity = _fixed_number(line, 44, 50)
                # Some valid CHIDRO rows leave Pot. blank; retain the asset
                # and represent the missing base capacity as zero.
                capacity = capacity if capacity is not None else 0.0
                db.add(EnergyAsset(
                    revision_id=revision.id, system_id=system.id if system else None, bus_code=asset_buses.get((suffix, "1", code)), source_code=code,
                    name=name.strip(), asset_type="hydro", technology="hydro",
                    capacity_mw=capacity, lifecycle_status="existing",
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
      for path in _canonical_family_files(root, f"{prefix}*.dat"):
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
                    r"^\s*(\d+)\s+(.{1,12}?)\s+(?P<units>\d+)\s+(?P<plant_type>\d+)\s+"
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
                    "unit_count": int(match.group("units")),
                    "plant_type": int(match.group("plant_type")),
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


def refresh_modification_payloads(root: Path, revision: StudyRevision, db: Session) -> int:
    """Backfill temporal fields for revisions imported before the richer parser."""
    refreshed = 0
    paths = {path.name.lower(): path for path in root.rglob("*") if path.is_file()}
    events = list(db.query(AssetModification).filter_by(revision_id=revision.id))
    for event in events:
        path = paths.get(event.source_file.lower())
        if path is None or event.entity_type not in {"thermal", "hydro", "renewable"}:
            continue
        lines = _read_lines(path)
        line = next((text for number, text in lines if number == event.source_line), None)
        if line is None:
            continue
        values: dict[str, object] | None = None
        if event.entity_type == "renewable":
            match = GEN_RE.match(line)
            if match:
                raw = match.groupdict()
                values = {
                    "name": raw["name"].strip(),
                    "capacity": raw["capacity"],
                    "factor": raw["factor"],
                    "plant_type": int(raw["plant_type"]) if raw["plant_type"] is not None else None,
                    "unit_count": int(raw["units"]),
                }
        else:
            match = re.match(
                r"^\s*(\d+)\s+(.{1,12}?)\s+(?P<units>\d+)\s+(?P<plant_type>\d+)\s+"
                r"(?P<capacity>[-+\d.Ee]+)\s+[-+\d.Ee]+\s+[-+\d.Ee]+\s+"
                r"(?P<teif>[-+\d.Ee]+)\s+(?P<ih>[-+\d.Ee]+)\s+(?P<variable_cost>[-+\d.Ee]+)",
                line,
            )
            if match:
                values = {"name": match.group(2).strip(), "capacity": match.group("capacity"), "unit_count": int(match.group("units")), "plant_type": int(match.group("plant_type")), "teif": match.group("teif"), "ih": match.group("ih"), "variable_cost": match.group("variable_cost")}
        if values:
            event.changed_fields_json = json.dumps(values, ensure_ascii=False)
            refreshed += 1
    db.flush()
    return refreshed


def _load_maintenance(root: Path, revision: StudyRevision, db: Session) -> int:
    """Parse PMHI/PMTR fixed-layout maintenance files without losing source rows."""
    count = 0
    language = _study_language_code(root)
    for path in sorted(root.rglob("pm*.dat")):
        name = path.name.lower()
        if not name.startswith(("pmhi", "pmtr")):
            continue
        asset_type = "hydro" if name.startswith("pmhi") else "thermal"
        file_match = re.match(r"^pm(?P<family>hi|tr)(?P<frequency>se|me)(?P<system>[^.]*)\.dat$", name, re.IGNORECASE)
        family = f"PM{file_match.group('family').upper()}" if file_match else ("PMHI" if name.startswith("pmhi") else "PMTR")
        frequency = "weekly" if file_match and file_match.group("frequency").lower() == "se" else "monthly"
        system_code = file_match.group("system").lower() if file_match and file_match.group("system") else None
        measure_type: int | None = None
        unit_type: int | None = None
        declared_measure_type: int | None = None
        declared_unit_type: int | None = None
        header_evidence: dict[str, object] = {}
        source_code: str | None = None
        asset_name = ""
        for line_number, line in _read_lines(path):
            info = re.search(rf"{localized_marker_pattern('info_type', language)}\s*\.?\s*:\s*(\d+)", line, re.IGNORECASE)
            if info:
                measure_type = int(info.group(1))
                declared_measure_type = measure_type
                header_evidence["info_type"] = {"value": measure_type, "line": line_number, "text": line.strip()}
                continue
            units = re.search(rf"{localized_marker_pattern('units', language)}\s*:\s*(\d+)", line, re.IGNORECASE)
            if units:
                unit_type = int(units.group(1))
                declared_unit_type = unit_type
                header_evidence["units"] = {"value": unit_type, "line": line_number, "text": line.strip()}
                continue
            plant = re.match(rf"^\*\*\*\*\s*{localized_marker_pattern('plant', language)}\s*:\s*(\d+)\s*(.*)$", line, re.IGNORECASE)
            if plant:
                source_code = plant.group(1)
                tokens = plant.group(2).split()
                pair = tokens[-2:] if len(tokens) >= 2 and all(token.isdigit() for token in tokens[-2:]) else []
                asset_name = " ".join(tokens[:-2] if pair else tokens)
                plant_measure_type = declared_measure_type
                plant_unit_type = declared_unit_type
                interpretation_status = "header"
                plant_warnings: list[str] = []
                if pair:
                    plant_unit_type, plant_measure_type = int(pair[0]), int(pair[1])
                    interpretation_status = "inferred"
                    if plant_unit_type not in {1, 2, 3, 4} or plant_measure_type not in {1, 2}:
                        plant_warnings.append("trailing plant configuration is outside documented Tipo Info./Unidades values")
                        plant_measure_type, plant_unit_type = measure_type, unit_type
                        interpretation_status = "header"
                    elif declared_measure_type is not None and declared_unit_type is not None and (plant_measure_type != declared_measure_type or plant_unit_type != declared_unit_type):
                        plant_warnings.append("trailing plant configuration differs from the file headers")
                if plant_measure_type is None:
                    plant_measure_type = 1
                    plant_warnings.append("maintenance measure type missing; defaulted to reduction")
                    interpretation_status = "defaulted"
                if plant_unit_type is None:
                    plant_unit_type = 2
                    plant_warnings.append("maintenance unit type missing; defaulted to percentage")
                    interpretation_status = "defaulted"
                header_evidence["plant"] = {
                    "family": family,
                    "frequency": frequency,
                    "system_code": system_code,
                    "plant_header": line.strip(),
                    "trailing_pair": {"unit_type": int(pair[0]), "measure_type": int(pair[1])} if pair else None,
                    "effective": {"unit_type": plant_unit_type, "measure_type": plant_measure_type},
                }
                header_evidence["plant_warnings"] = plant_warnings
                measure_type, unit_type = plant_measure_type, plant_unit_type
                continue
            values = line.split()
            if not values or not values[0].isdigit() or source_code is None:
                continue
            year = int(values[0])
            stage_values = [_number(value) for value in values[1:]]
            warnings: list[str] = list(header_evidence.get("plant_warnings", []))
            if measure_type is None:
                measure_type = 1
                warnings.append("maintenance measure type missing; defaulted to reduction")
            if unit_type is None:
                unit_type = 2
                warnings.append("maintenance unit type missing; defaulted to percentage")
            if not stage_values:
                warnings.append("maintenance row has no stage values")
            if unit_type == 1 and any(value < 0 or not value.is_integer() for value in stage_values):
                warnings.append("maintenance uses number-of-units but contains a non-integral or out-of-range value; value will not be applied")
            db.add(StudyMaintenance(
                revision_id=revision.id,
                asset_type=asset_type,
                source_code=source_code,
                asset_name=asset_name,
                measure_type=measure_type,
                unit_type=unit_type,
                year=year,
                stage_values_json=json.dumps(stage_values),
                source_file=path.name,
                source_line=line_number,
                warnings_json=json.dumps(warnings),
                family=family,
                frequency=frequency,
                system_code=system_code,
                header_evidence_json=json.dumps(header_evidence, ensure_ascii=False),
                interpretation_status="inferred" if header_evidence.get("plant", {}).get("trailing_pair") else "header",
                review_status="pending",
            ))
            count += 1
    db.flush()
    return count


def _load_demands(root: Path, revision: StudyRevision, systems: dict[str, StudySystem], db: Session) -> int:
    count = 0
    language = _study_language_code(root)
    for path in _files(root, "deme*.dat"):
        suffix_match = re.search(r"deme\d+[a-z]+$", path.stem.lower())
        suffix = re.sub(r"^deme\d+", "", suffix_match.group()) if suffix_match else path.stem[4:].lower()
        system = systems.get(suffix) or systems.get("")
        current_code: str | None = None
        current_segment = 1
        for line_number, line in _read_lines(path):
            header = re.match(rf"^\*\*\*\*\s*{localized_marker_pattern('load', language)}\s*:\s*(\d+)\s+.*?Sgmnt:\s*(\d+)", line, re.IGNORECASE)
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


def _load_demand_definitions(root: Path, revision: StudyRevision, systems: dict[str, StudySystem], db: Session) -> int:
    count = 0
    for path in _files(root, "cloads*.dat"):
        suffix = path.stem[len("cloads"):].lower()
        system = systems.get(suffix) or systems.get("")
        for line_number, line in _read_lines(path):
            if not line[:4].strip().isdigit():
                continue
            try:
                code = line[:4].strip()
                name = line[5:17].strip()
                segment_count = int(line[18:23].strip())
                segment_type = int(line[24:29].strip()) if line[24:29].strip() else None
            except ValueError:
                continue
            db.add(StudyDemandDefinition(revision_id=revision.id, system_id=system.id if system else None, source_code=code, name=name or code, segment_count=segment_count, first_segment_type=segment_type, source_file=path.name, source_line=line_number))
            count += 1
    db.flush()
    return count


def _load_batteries(root: Path, revision: StudyRevision, systems: dict[str, StudySystem], db: Session) -> tuple[int, int]:
    assets = modifications = 0
    for path in _canonical_family_files(root, "cbattery*.dat"):
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
    for path in _canonical_family_files(root, "mbattery*.dat"):
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


def _load_fuels(root: Path, revision: StudyRevision, systems: dict[str, StudySystem], db: Session) -> tuple[int, int]:
    fuels = prices = 0
    language = _study_language_code(root)
    for path in _files(root, "ccombu*.dat"):
        suffix = path.stem[len("ccombu"):].lower()
        system = systems.get(suffix) or systems.get("")
        for line_number, line in _read_lines(path):
            if not line[:4].strip().isdigit():
                continue
            try:
                code = line[:4].strip()
                name = line[5:17].strip() or code
                unit = line[18:25].strip() or None
                cost = _optional_number(line[26:34])
                co2 = _optional_number(line[35:41])
            except (IndexError, ValueError):
                continue
            db.add(StudyFuel(revision_id=revision.id, system_id=system.id if system else None, source_code=code, name=name, unit_name=unit, base_cost=cost, co2_factor=co2, source_file=path.name, source_line=line_number))
            fuels += 1
    for path in _files(root, "combme*.dat"):
        current_code: str | None = None
        for line_number, line in _read_lines(path):
            header = re.search(rf"{localized_marker_pattern('fuel', language)}\s*:\s*(\d+)", line, re.IGNORECASE)
            if header:
                current_code = header.group(1)
                continue
            if current_code is None or not line[:4].strip().isdigit():
                continue
            values = line.split()
            try:
                year = int(values[0])
                for month, raw in enumerate(values[1:13], start=1):
                    if raw.strip():
                        db.add(StudyFuelPrice(revision_id=revision.id, fuel_code=current_code, year=year, month=month, price=_number(raw), source_file=path.name, source_line=line_number))
                        prices += 1
            except (ValueError, IndexError):
                continue
    db.flush()
    return fuels, prices


def _load_currencies(root: Path, revision: StudyRevision, db: Session) -> int:
    path = _find(root, "unimon.dat")
    if path is None:
        return 0
    reference: str | None = None
    count = 0
    for line_number, line in _read_lines(path):
        if line.upper().startswith("$UREF"):
            fields = line.split()
            reference = fields[-1] if len(fields) > 1 else None
            continue
        fields = line.split()
        if len(fields) < 2 or len(fields[0]) > 3:
            continue
        try:
            conversion = float(fields[1].replace(",", "."))
        except ValueError:
            continue
        db.add(StudyCurrency(revision_id=revision.id, code=fields[0], conversion_to_reference=conversion, is_reference=fields[0] == reference, source_file=path.name, source_line=line_number))
        count += 1
    db.flush()
    return count


def build_intermediate_model(root: str | Path, revision: StudyRevision, db: Session) -> dict[str, int]:
    root_path = Path(root)
    systems = _load_systems(root_path, revision, db)
    buses = _load_buses(root_path, revision, systems, db)
    assets = _load_base_assets(root_path, revision, systems, db)
    generator_details = _load_generator_details(root_path, revision, db)
    renewable_profiles = _load_renewable_profiles(root_path, revision, db)
    renewable_assignments = _load_renewable_assignments(root_path, revision, systems, db)
    hydro_inputs = _load_hydro_inputs(root_path, revision, db)
    circuits = _load_circuits(root_path, revision, db)
    modifications = _load_modifications(root_path, revision, db)
    refreshed_modifications = refresh_modification_payloads(root_path, revision, db)
    maintenance = _load_maintenance(root_path, revision, db)
    demands = _load_demands(root_path, revision, systems, db)
    demand_definitions = _load_demand_definitions(root_path, revision, systems, db)
    batteries, battery_modifications = _load_batteries(root_path, revision, systems, db)
    bus_demands = _load_bus_demands(root_path, revision, db)
    hourly_demand = _load_hourly_demand_inputs(root_path, revision, db)
    fuels, fuel_prices = _load_fuels(root_path, revision, systems, db)
    currencies = _load_currencies(root_path, revision, db)
    descriptor = db.query(StudyDescriptor).filter_by(revision_id=revision.id).first()
    if descriptor:
        warnings = json.loads(descriptor.warnings_json or "[]")
        unsupported = {
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
    return {"systems": len(systems), "buses": len(buses), "assets": assets, **generator_details, "renewable_profiles": renewable_profiles, "renewable_assignments": renewable_assignments, **hydro_inputs, "circuits": circuits,
            "modifications": modifications + battery_modifications, "refreshed_modifications": refreshed_modifications, "maintenance": maintenance, "demands": demands, "demand_definitions": demand_definitions, "bus_demands": bus_demands, **hourly_demand, "fuels": fuels, "fuel_prices": fuel_prices, "currencies": currencies, "batteries": batteries}
