import json
from calendar import monthrange
from datetime import UTC, datetime

from sqlalchemy import select
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


def _stage_date(stage: int, year: int = 2023) -> datetime:
    month_index = max(stage - 1, 0)
    result_year = year + month_index // 12
    month = month_index % 12 + 1
    return datetime(result_year, month, min(1, monthrange(result_year, month)[1]), tzinfo=UTC)


def effective_snapshot(revision: StudyRevision, stage: int, block: int | None, db: Session) -> dict[str, object]:
    """Return the current input state. Stage-to-date mapping is explicit and auditable."""
    # Monthly SDDP studies use the first day of the corresponding stage here.
    descriptor = db.scalar(select(StudyDescriptor).where(
        StudyDescriptor.project_id == revision.project_id,
        StudyDescriptor.revision_id == revision.id,
    )) or db.scalar(select(StudyDescriptor).where(
        StudyDescriptor.project_id == revision.project_id,
        StudyDescriptor.revision_id.is_(None),
    ).order_by(StudyDescriptor.created_at.desc()))
    study_metadata = {}
    if descriptor:
        study_metadata = json.loads(descriptor.descriptor_json)
    initial_year = int(study_metadata.get("ano inicial", 2023))
    date = _stage_date(stage, initial_year)
    assets = list(db.scalars(select(EnergyAsset).where(EnergyAsset.revision_id == revision.id)))
    buses = list(db.scalars(select(StudyBus).where(StudyBus.revision_id == revision.id)))
    warnings = json.loads(descriptor.warnings_json) if descriptor else ["study descriptor unavailable"]
    systems = list(db.scalars(select(StudySystem).where(StudySystem.revision_id == revision.id)))
    demands = list(db.scalars(select(StudyDemand).where(StudyDemand.revision_id == revision.id)))
    bus_demands = list(db.scalars(select(StudyBusDemand).where(StudyBusDemand.revision_id == revision.id, StudyBusDemand.effective_date <= date, StudyBusDemand.block == (block or 1))))
    bus_demand_by_code = {item.bus_code: item.demand_mw for item in bus_demands}
    if not demands and not any(json.loads(bus.demand_block_mw_json) for bus in buses):
        warnings.append("Demand values are not available in the intermediate model; DBF/DEME series require a validated decoder.")
    buses_by_code = {bus.source_code: bus for bus in buses}
    modifications = list(db.scalars(select(AssetModification).where(
        AssetModification.revision_id == revision.id,
        AssetModification.effective_date <= date,
    ).order_by(AssetModification.effective_date, AssetModification.sequence)))
    asset_rows = []
    for asset in assets:
        events = [item for item in modifications if item.entity_type == asset.asset_type and item.source_code == asset.source_code]
        capacity = asset.capacity_mw
        operating_factor = asset.operating_factor
        lifecycle_status = asset.lifecycle_status
        asset_bus = asset.bus_code
        applied_events = []
        for event in events:
            payload = json.loads(event.changed_fields_json)
            if payload.get("capacity") is not None:
                capacity = float(payload["capacity"])
            if payload.get("bus") is not None:
                asset_bus = str(payload["bus"])
            else:
                asset_bus = asset.bus_code
            if payload.get("factor") is not None:
                operating_factor = float(payload["factor"])
            if payload.get("existing") is not None:
                lifecycle_status = "future" if str(payload["existing"]) == "1" else "existing"
            if payload.get("plant_type") is not None:
                lifecycle_status = "future" if str(payload["plant_type"]) == "1" else "existing"
            applied_events.append({"source_file": event.source_file, "source_line": event.source_line, "effective_date": event.effective_date.date().isoformat()})
        row = {
            "id": asset.id, "source_code": asset.source_code, "name": asset.name,
            "asset_type": asset.asset_type, "technology": asset.technology,
            "bus_code": asset_bus,
            "system_code": next((system.code for system in systems if system.id == asset.system_id), None),
            "bus": int(asset_bus) if asset_bus and asset_bus.isdigit() else None,
            "latitude": buses_by_code[asset_bus].latitude if asset_bus in buses_by_code else None,
            "longitude": buses_by_code[asset_bus].longitude if asset_bus in buses_by_code else None,
            "coordinate_status": "bus-reference" if asset_bus in buses_by_code else "not-provided",
            "capacity_mw": capacity, "operating_factor": operating_factor, "lifecycle_status": lifecycle_status,
            "is_active": lifecycle_status == "existing" and (capacity or 0) > 0,
            "source_file": asset.source_file, "source_line": asset.source_line,
            "modifications": applied_events,
        }
        asset_rows.append(row)
    primary_by_bus: dict[str, dict[str, object]] = {}
    for row in asset_rows:
        bus_code = row.get("bus_code")
        if not bus_code or not row["is_active"]:
            continue
        current = primary_by_bus.get(str(bus_code))
        if current is None or (row["capacity_mw"] or 0) > (current["capacity_mw"] or 0):
            primary_by_bus[str(bus_code)] = {
                "source_code": row["source_code"],
                "name": row["name"],
                "technology": row["technology"],
                "capacity_mw": row["capacity_mw"],
            }
    circuits = list(db.scalars(select(StudyCircuit).where(StudyCircuit.revision_id == revision.id)))
    system_by_bus = {bus.source_code: next((system.code for system in systems if system.id == bus.system_id), None) for bus in buses}
    demand_rows = []
    for demand in demands:
        if demand.year != date.year or demand.block != (block or 1):
            continue
        monthly = json.loads(demand.monthly_gwh_json)
        value = monthly[date.month - 1] if len(monthly) >= date.month else None
        demand_rows.append({"source_code": demand.source_code, "segment": demand.segment, "system_code": next((system.code for system in systems if system.id == demand.system_id), None), "year": demand.year, "block": demand.block, "value_gwh": value, "source_file": demand.source_file, "source_line": demand.source_line})
    maintenance = []
    stage_index = date.month
    for item in db.scalars(select(StudyMaintenance).where(
        StudyMaintenance.revision_id == revision.id,
        StudyMaintenance.year == date.year,
    )):
        values = json.loads(item.stage_values_json)
        maintenance.append({
            "asset_type": item.asset_type,
            "source_code": item.source_code,
            "asset_name": item.asset_name,
            "measure_type": item.measure_type,
            "unit_type": item.unit_type,
            "year": item.year,
            "value": values[stage_index - 1] if len(values) >= stage_index else None,
            "source_file": item.source_file,
            "source_line": item.source_line,
            "warnings": json.loads(item.warnings_json),
        })
    return {
        "stage": stage, "block": block, "as_of": date.date().isoformat(),
        "study": {
            "initial_year": initial_year,
            "stages": int(study_metadata.get("numero de etapas", 0) or 0),
            "blocks": int((study_metadata.get("numero de bloques demanda") or [0])[0]),
            "frequency": "weekly" if study_metadata.get("etapa") == 1 else "monthly",
            "block_durations_hours": study_metadata.get("block_durations_hours", {}),
             "warnings": warnings,
            "systems": [{"code": system.code, "name": system.name, "country_code": system.country_code} for system in systems],
            "layout": "geographic map" if any(bus.latitude is not None and bus.longitude is not None for bus in buses) else "topology layout",
        },
        "entities": asset_rows,
        "buses": [
             {"source_code": bus.source_code, "name": bus.name, "system_code": system_by_bus.get(bus.source_code), "nominal_voltage_kv": bus.nominal_voltage_kv, "demand_mw": bus_demand_by_code.get(bus.source_code, json.loads(bus.demand_block_mw_json).get(str(block or 1), 0)), "primary_source": primary_by_bus.get(bus.source_code), "latitude": bus.latitude, "longitude": bus.longitude,
             "coordinate_source": bus.coordinate_source, "source_file": bus.source_file, "source_line": bus.source_line}
            for bus in buses
        ],
        "circuits": [
             {"source_code": circuit.source_code, "from_bus": circuit.from_bus, "to_bus": circuit.to_bus,
              "system_code": system_by_bus.get(circuit.from_bus), "from_system_code": system_by_bus.get(circuit.from_bus), "to_system_code": system_by_bus.get(circuit.to_bus), "is_interconnection": system_by_bus.get(circuit.from_bus) != system_by_bus.get(circuit.to_bus),
              "from_latitude": buses_by_code.get(circuit.from_bus).latitude if buses_by_code.get(circuit.from_bus) else None, "from_longitude": buses_by_code.get(circuit.from_bus).longitude if buses_by_code.get(circuit.from_bus) else None, "to_latitude": buses_by_code.get(circuit.to_bus).latitude if buses_by_code.get(circuit.to_bus) else None, "to_longitude": buses_by_code.get(circuit.to_bus).longitude if buses_by_code.get(circuit.to_bus) else None, "nominal_voltage_kv": circuit.nominal_voltage_kv, "voltage_source": circuit.voltage_source,
              "name": circuit.name, "normal_limit_mw": circuit.normal_limit_mw,
              "emergency_limit_mw": circuit.emergency_limit_mw, "status": circuit.status, "source_file": circuit.source_file, "source_line": circuit.source_line}
            for circuit in circuits
        ],
        "maintenance": maintenance,
        "demands": demand_rows,
        "provenance": "intermediate database snapshot",
    }
