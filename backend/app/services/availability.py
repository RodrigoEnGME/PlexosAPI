"""Single source of truth for maintenance and outage availability semantics."""

import json
from typing import Any

from app.services.snapshot import _maintenance_matches, _maintenance_value_is_valid


def calculate_availability(
    maximum: float,
    detail: dict[str, Any],
    maintenance: list[Any],
    *,
    year: int,
    stage_index: int,
    basis: str = "short_term",
    asset_name: str = "",
    asset_type: str = "",
    source_code: str = "",
    system_code: str | None = None,
    system_country_code: str | None = None,
) -> dict[str, Any]:
    valid_system_codes = {value for value in (system_code, system_country_code) if value}
    plans = [item for item in maintenance if item.asset_type == asset_type and item.source_code == source_code and (not getattr(item, "system_code", None) or not valid_system_codes or item.system_code in valid_system_codes) and (not item.asset_name or _maintenance_matches(asset_name, item.asset_name))]
    matching = [item for item in plans if item.year == year]
    has_plan = bool(plans)
    item = matching[-1] if matching else (plans[-1] if plans else None)
    value = None
    if item:
        values = json.loads(item.stage_values_json)
        value = values[stage_index - 1] if len(values) >= stage_index else None
    result = {"available": None, "source": "unresolved", "warning": None, "maintenance": item, "value": value, "has_maintenance_plan": has_plan}
    if has_plan:
        if not matching:
            result["warning"] = "Maintenance plan has no applicable value for this year."
            return result
        if value is None:
            result["warning"] = "Maintenance plan has no applicable value for this year/stage."
            return result
        try:
            value = float(value)
        except (TypeError, ValueError):
            result["warning"] = "Maintenance plan value is not numeric."
            return result
        unit = int(item.unit_type or 0)
        if unit == 4:
            result["warning"] = "Maintenance unit m3/s cannot be converted to MW; availability is unresolved."
            return result
        if not _maintenance_value_is_valid(value, unit, detail):
            result["warning"] = "Maintenance value is incompatible with its declared unit."
            return result
        if item.measure_type == 2:
            available = maximum * value / 100 if unit == 2 else value if unit == 3 else maximum * value / max(1, int(detail.get("unit_count") or 1))
        elif item.measure_type == 1:
            reduction = maximum * value / 100 if unit == 2 else value if unit == 3 else maximum * value / max(1, int(detail.get("unit_count") or 1))
            available = maximum - reduction
        else:
            result["warning"] = "Maintenance measure type is unsupported."
            return result
        result.update({"available": max(0.0, available), "source": "maintenance_plan"})
        return result
    index = detail.get("short_term_outage_pct") if basis == "short_term" else detail.get("historical_outage_pct")
    # Legacy detail rows may omit an outage index; SDDP's absence means no
    # additional outage, while the source remains the selected basis.
    index = float(index or 0)
    result.update({"available": maximum * max(0.0, 1.0 - float(index) / 100.0), "source": f"{basis}_outage_index"})
    return result
