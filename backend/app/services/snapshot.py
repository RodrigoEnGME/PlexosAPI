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
    StudyCurrency,
    StudyDemand,
    StudyDemandDefinition,
    StudyDescriptor,
    StudyFuel,
    StudyFuelPrice,
    StudyHydroDetail,
    StudyMaintenance,
    StudyRenewableDetail,
    StudyRevision,
    StudySystem,
    StudyThermalDetail,
)


def _normalized_label(value: str | None) -> str:
    return " ".join((value or "").replace("_", " ").casefold().split())


def _maintenance_matches(asset_name: str, maintenance_name: str) -> bool:
    asset_label = _normalized_label(asset_name)
    maintenance_tokens = _normalized_label(maintenance_name).split()
    # PMHI/PMTR rows append unit/type columns after the plant name.
    while len(maintenance_tokens) > 1 and all(token.isdigit() for token in maintenance_tokens[-2:]):
        maintenance_tokens = maintenance_tokens[:-2]
    return asset_label == " ".join(maintenance_tokens)


def _maintenance_value_is_valid(value: float, unit_type: int, detail: dict[str, object]) -> bool:
    if value < 0 or unit_type != 1:
        return value >= 0
    unit_count = int(detail.get("unit_count") or 0)
    return unit_count > 0 and value <= unit_count and value.is_integer()


def _modification_applies(asset_name: str, event: AssetModification) -> bool:
    payload = json.loads(event.changed_fields_json)
    event_name = payload.get("name")
    return not event_name or _normalized_label(asset_name) == _normalized_label(str(event_name))


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
    warnings = [warning for warning in (json.loads(descriptor.warnings_json) if descriptor else ["study descriptor unavailable"]) if "Hydrological topology is inventoried" not in warning and "Natural inflow series is inventoried" not in warning]
    systems = list(db.scalars(select(StudySystem).where(StudySystem.revision_id == revision.id)))
    demands = list(db.scalars(select(StudyDemand).where(StudyDemand.revision_id == revision.id)))
    demand_definitions = list(db.scalars(select(StudyDemandDefinition).where(StudyDemandDefinition.revision_id == revision.id)))
    fuels = list(db.scalars(select(StudyFuel).where(StudyFuel.revision_id == revision.id)))
    fuel_prices = list(db.scalars(select(StudyFuelPrice).where(StudyFuelPrice.revision_id == revision.id, StudyFuelPrice.year == date.year, StudyFuelPrice.month == date.month)))
    currencies = list(db.scalars(select(StudyCurrency).where(StudyCurrency.revision_id == revision.id)))
    thermal_details = {item.source_code: item for item in db.scalars(select(StudyThermalDetail).where(StudyThermalDetail.revision_id == revision.id))}
    hydro_details = {item.source_code: item for item in db.scalars(select(StudyHydroDetail).where(StudyHydroDetail.revision_id == revision.id))}
    renewable_details = {item.source_code: item for item in db.scalars(select(StudyRenewableDetail).where(StudyRenewableDetail.revision_id == revision.id))}
    definition_keys = {(item.system_id, item.source_code) for item in demand_definitions}
    demand_code_refs = {(item.system_id, item.source_code) for item in demands}
    demand_code_refs.update({(next((bus.system_id for bus in buses if bus.source_code == item.bus_code), None), item.demand_code) for item in db.scalars(select(StudyBusDemand).where(StudyBusDemand.revision_id == revision.id))})
    for system_id, code in sorted(demand_code_refs - definition_keys):
        warnings.append(f"Demand code {code} has no CLOADS definition for its source system.")
    bus_demands = list(db.scalars(select(StudyBusDemand).where(StudyBusDemand.revision_id == revision.id, StudyBusDemand.effective_date <= date, StudyBusDemand.block == (block or 1))))
    bus_demand_by_code = {item.bus_code: item.demand_mw for item in bus_demands}
    if not demands and not bus_demands and not any(json.loads(bus.demand_block_mw_json) for bus in buses):
        warnings.append("Demand values are not available for this revision; no DEME, DBF or DBUS demand records were found.")
    buses_by_code = {bus.source_code: bus for bus in buses}
    modifications = list(db.scalars(select(AssetModification).where(
        AssetModification.revision_id == revision.id,
        AssetModification.effective_date <= date,
    ).order_by(AssetModification.effective_date, AssetModification.sequence)))
    asset_rows = []
    for asset in assets:
        events = [item for item in modifications if item.entity_type == asset.asset_type and item.source_code == asset.source_code and _modification_applies(asset.name, item)]
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
        thermal = thermal_details.get(asset.source_code)
        hydro = hydro_details.get(asset.source_code)
        renewable = renewable_details.get(asset.source_code)
        if thermal:
            row["technical_details"] = {"kind": "thermal", "unit_count": thermal.unit_count, "plant_type": thermal.plant_type, "min_generation_mw": thermal.min_generation_mw, "max_generation_mw": thermal.max_generation_mw, "short_term_outage_pct": thermal.short_term_outage_pct, "historical_outage_pct": thermal.historical_outage_pct, "variable_om_cost": thermal.variable_om_cost, "fuel_code": thermal.fuel_code, "consumption_segments": json.loads(thermal.consumption_segments_json), "alternative_fuels": json.loads(thermal.alternative_fuels_json), "commitment_type": thermal.commitment_type, "transport_cost": thermal.transport_cost, "startup_cost": thermal.startup_cost, "gas_system": thermal.gas_system, "combined_cycle_code": thermal.combined_cycle_code, "emission_factor": thermal.emission_factor, "source_file": thermal.source_file, "source_line": thermal.source_line}
        elif hydro:
            row["technical_details"] = {"kind": "hydro", "station_code": hydro.station_code, "downstream_spill_code": hydro.downstream_spill_code, "downstream_turbine_code": hydro.downstream_turbine_code, "unit_count": hydro.unit_count, "plant_type": hydro.plant_type, "production_factor": hydro.production_factor, "min_turbine_flow": hydro.min_turbine_flow, "max_turbine_flow": hydro.max_turbine_flow, "min_volume_hm3": hydro.min_volume_hm3, "max_volume_hm3": hydro.max_volume_hm3, "initial_condition": hydro.initial_condition, "min_total_flow": hydro.min_total_flow, "spill_mode": hydro.spill_mode, "short_term_outage_pct": hydro.short_term_outage_pct, "historical_outage_pct": hydro.historical_outage_pct, "production_curve": json.loads(hydro.production_curve_json), "level_volume_curve": json.loads(hydro.level_volume_curve_json), "source_file": hydro.source_file, "source_line": hydro.source_line}
        elif renewable:
            row["technical_details"] = {"kind": "renewable", "unit_count": renewable.unit_count, "plant_type": renewable.plant_type, "operating_factor": renewable.operating_factor, "failure_probability": renewable.failure_probability, "technology_type": renewable.technology_type, "source_file": renewable.source_file, "source_line": renewable.source_line}
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
    is_weekly = study_metadata.get("etapa") == 1
    stage_index = stage if is_weekly else date.month
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
    for row in asset_rows:
        detail = row.get("technical_details") or {}
        maintenance_item = next((item for item in maintenance if item["value"] is not None and item["asset_type"] == row["asset_type"] and item["source_code"] == row["source_code"] and (not item["asset_name"] or _maintenance_matches(row["name"], item["asset_name"]))), None)
        installed = row["capacity_mw"] or 0.0
        # Availability follows the effective installed capacity. Technical
        # maximums describe the base input, but dated capacity changes must
        # affect the capacity available at the selected stage.
        max_generation = installed or detail.get("max_generation_mw") or 0.0
        maintenance_mode = study_metadata.get("maintenance_mode")
        outage = 0 if maintenance_mode == "schedule" else max(
            float(detail.get("short_term_outage_pct") or 0),
            float(detail.get("historical_outage_pct") or 0),
        )
        available = max_generation * max(0.0, 1.0 - outage / 100.0)
        maintenance_reduction = 0.0
        if maintenance_item:
            value = float(maintenance_item["value"])
            valid_maintenance = _maintenance_value_is_valid(value, maintenance_item["unit_type"], detail)
            if valid_maintenance and maintenance_item["measure_type"] == 2:
                if maintenance_item["unit_type"] == 2:
                    available = max_generation * value / 100.0
                elif maintenance_item["unit_type"] == 3:
                    available = value
                elif maintenance_item["unit_type"] == 1:
                    units = detail.get("unit_count") or 1
                    available = max_generation * max(0.0, min(1.0, value / units))
            elif valid_maintenance and maintenance_item["measure_type"] == 1:
                if maintenance_item["unit_type"] == 2:
                    maintenance_reduction = max_generation * value / 100.0
                elif maintenance_item["unit_type"] == 3:
                    maintenance_reduction = value
                elif maintenance_item["unit_type"] == 1:
                    units = detail.get("unit_count") or 1
                    maintenance_reduction = max_generation * min(1.0, value / units)
                available = max(0.0, available - maintenance_reduction)
        row["capacity_installed_mw"] = installed
        row["capacity_maximum_mw"] = max_generation
        row["capacity_available_mw"] = max(0.0, available) if row["is_active"] else 0.0
        row["maintenance_value"] = maintenance_item["value"] if maintenance_item else None
        row["maintenance_type"] = maintenance_item["measure_type"] if maintenance_item else None
        row["maintenance_unit"] = maintenance_item["unit_type"] if maintenance_item else None
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
        "demand_definitions": [{"source_code": item.source_code, "name": item.name, "segment_count": item.segment_count, "first_segment_type": item.first_segment_type, "system_code": next((system.code for system in systems if system.id == item.system_id), None), "source_file": item.source_file, "source_line": item.source_line} for item in demand_definitions],
        "fuels": [{"source_code": item.source_code, "name": item.name, "unit_name": item.unit_name, "base_cost": item.base_cost, "co2_factor": item.co2_factor, "system_code": next((system.code for system in systems if system.id == item.system_id), None), "source_file": item.source_file, "source_line": item.source_line} for item in fuels],
        "fuel_prices": [{"fuel_code": item.fuel_code, "year": item.year, "month": item.month, "price": item.price, "source_file": item.source_file, "source_line": item.source_line} for item in fuel_prices],
        "currencies": [{"code": item.code, "conversion_to_reference": item.conversion_to_reference, "is_reference": item.is_reference, "source_file": item.source_file, "source_line": item.source_line} for item in currencies],
        "provenance": "intermediate database snapshot",
    }
