"""Versioned semantic schemas derived from the documented input catalog."""

import re
from dataclasses import asdict, dataclass, replace
from pathlib import Path

from app.services.input_catalog import InputFieldSpec, load_input_dictionary
from app.services.language_profile import canonical_label

SCHEMA_VERSION = "sddp-17.2-dictionary-v0"


@dataclass(frozen=True, slots=True)
class SchemaField:
    key: str
    attribute: str
    source_name: str
    aliases: tuple[str, ...]
    data_type: str
    source_unit: str
    target_unit: str
    source_row: int
    status: str
    position_start: int | None = None
    position_end: int | None = None

    def as_dict(self) -> dict[str, object]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class FamilySchema:
    family: str
    source_pattern: str
    version: str
    layout: str
    encoding: str
    key_fields: tuple[str, ...]
    fields: tuple[SchemaField, ...]
    documentation_source: str

    @property
    def status(self) -> str:
        statuses = {field.status for field in self.fields}
        if "needs-validation" in statuses:
            return "schema-documented"
        return "validated"

    def as_dict(self) -> dict[str, object]:
        result = asdict(self)
        result["status"] = self.status
        return result


FAMILY_METADATA: dict[str, tuple[str, str, str, tuple[str, ...]]] = {
    "ctermi": ("ctermi*.dat", "fixed-width", "latin-1", ("source_code",)),
    "chidro": ("chidro*.dat", "fixed-width", "latin-1", ("source_code",)),
    "cgnd": ("cgnd*.dat", "fixed-width", "latin-1", ("source_code",)),
    "dbus": ("dbus.dat", "fixed-width", "latin-1", ("source_code",)),
    "dcirc": ("dcirc.dat", "fixed-width", "latin-1", ("source_code",)),
    "dgbus": ("dgbus.dat", "fixed-width", "latin-1", ("source_code",)),
    "ccombu": ("ccombu*.dat", "fixed-width", "latin-1", ("source_code",)),
    "combme": ("combme*.dat", "table", "latin-1", ("source_code", "year", "month")),
    "cloads": ("cloads*.dat", "fixed-width", "latin-1", ("source_code",)),
    "dbf": ("dbf*.dat", "fixed-width", "latin-1", ("bus_code", "demand_code", "date", "block")),
    "gndsite": ("gndsite*.dat", "table", "latin-1", ("site_code",)),
    "hrload": ("hrload*.dat", "csv-or-table", "latin-1", ("year", "month", "hour", "load_code")),
    "hrrenw": ("hrrenw*.dat", "csv-or-table", "latin-1", ("scenario", "year", "month", "hour")),
    "hinflw": ("hinflw*.dat", "fixed-width-table", "latin-1", ("year", "month", "station_code")),
    "hrbmap": ("hrbmap*.dat", "csv-or-table", "latin-1", ("year", "month", "hour")),
    "htopol": ("htopol.dat", "fixed-width", "latin-1", ("station_code",)),
    "volt": ("volt.dat", "fixed-width", "latin-1", ("bus_code",)),
    "sistem": ("sistem.dat", "whitespace", "latin-1", ("system_code",)),
    "pmhi": ("pmhi*.dat", "block-table", "latin-1", ("source_code", "year", "stage")),
    "pmtr": ("pmtr*.dat", "block-table", "latin-1", ("source_code", "year", "stage")),
    "mtermi": ("mtermi*.dat", "dated-fixed-width", "latin-1", ("source_code", "effective_date")),
    "mhidro": ("mhidro*.dat", "dated-fixed-width", "latin-1", ("source_code", "effective_date")),
    "mgnd": ("mgnd*.dat", "dated-fixed-width", "latin-1", ("source_code", "effective_date")),
    "mcirc": ("mcirc.dat", "dated-fixed-width", "latin-1", ("source_code", "effective_date")),
    "sddp": ("sddp.dat", "control", "detected", ("language", "initial_year", "stages")),
}


CHIDRO_LAYOUT_BY_ROW: dict[int, tuple[int, int]] = {
    15: (1, 4),
    16: (6, 17),
    17: (19, 22),
    18: (24, 27),
    19: (29, 32),
    20: (34, 37),
    21: (39, 42),
    22: (44, 50),
    23: (52, 58),
    24: (60, 66),
    25: (68, 74),
    26: (76, 82),
    27: (84, 90),
    28: (92, 98),
    29: (553, 559),
}


def _family_for_file(source_file: str) -> str:
    stem = Path(source_file).stem.casefold()
    return next((family for family in FAMILY_METADATA if stem.startswith(family)), stem)


def _key(entry: InputFieldSpec) -> str:
    canonical = canonical_label(entry.sddp_name)
    raw = canonical or entry.attribute
    return re.sub(r"[^a-z0-9]+", "_", raw.casefold()).strip("_") or "unnamed"


def _field(entry: InputFieldSpec) -> SchemaField:
    aliases = tuple(dict.fromkeys((entry.sddp_name, canonical_label(entry.sddp_name) or "")))
    family = _family_for_file(entry.source_file)
    position = CHIDRO_LAYOUT_BY_ROW.get(entry.source_row) if family == "chidro" else None
    return SchemaField(
        key=_key(entry),
        attribute=entry.attribute,
        source_name=entry.sddp_name,
        aliases=tuple(alias for alias in aliases if alias),
        data_type=entry.sddp_type,
        source_unit=entry.sddp_unit,
        target_unit=entry.plexos_unit,
        source_row=entry.source_row,
        status="validated" if position else "needs-validation",
        position_start=position[0] if position else None,
        position_end=position[1] if position else None,
    )


def build_schema_registry(dictionary_path: str | Path) -> dict[str, FamilySchema]:
    """Build the initial family registry without inventing field offsets."""
    entries = load_input_dictionary(dictionary_path)
    registry: dict[str, FamilySchema] = {}
    for entry in entries:
        if entry.source_file in {"", "-"}:
            continue
        family = _family_for_file(entry.source_file)
        pattern, layout, encoding, key_fields = FAMILY_METADATA.get(
            family,
            (entry.source_file, "undocumented", "detected", ()),
        )
        current = registry.get(family)
        field = _field(entry)
        if current and field.key in {item.key for item in current.fields}:
            source_key = re.sub(r"[^a-z0-9]+", "_", entry.sddp_name.casefold()).strip("_")
            field = replace(field, key=f"{field.key}_{source_key}")
        fields = (*current.fields, field) if current else (field,)
        registry[family] = FamilySchema(
            family=family,
            source_pattern=pattern,
            version=SCHEMA_VERSION,
            layout=layout,
            encoding=encoding,
            key_fields=key_fields,
            fields=fields,
            documentation_source=Path(dictionary_path).name,
        )
    return registry


def validate_schema_registry(registry: dict[str, FamilySchema]) -> None:
    for family, schema in registry.items():
        if not schema.fields:
            raise ValueError(f"schema has no fields: {family}")
        keys: set[str] = set()
        for field in schema.fields:
            if field.key in keys:
                raise ValueError(f"duplicate schema field {family}.{field.key}")
            keys.add(field.key)
        if not schema.version or not schema.source_pattern:
            raise ValueError(f"schema metadata is incomplete: {family}")


def schema_registry_as_dict(dictionary_path: str | Path) -> dict[str, object]:
    registry = build_schema_registry(dictionary_path)
    validate_schema_registry(registry)
    return {family: schema.as_dict() for family, schema in registry.items()}
