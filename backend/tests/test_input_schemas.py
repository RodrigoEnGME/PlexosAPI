from pathlib import Path

from app.services.input_schemas import (
    build_schema_registry,
    schema_registry_as_dict,
    validate_schema_registry,
)
from app.services.intermediate_model import _fixed_int, _fixed_number


def test_builds_versioned_schema_registry_from_dictionary() -> None:
    path = Path(__file__).resolve().parents[2] / "data/20250207_Diccionario_SDDP_PLEXOS_v0.xlsx"
    registry = build_schema_registry(path)
    validate_schema_registry(registry)
    payload = schema_registry_as_dict(path)

    assert {"ctermi", "chidro", "cgnd", "dbus", "dbf", "mhidro", "pmhi"}.issubset(registry)
    assert registry["chidro"].version == "sddp-17.2-dictionary-v0"
    assert registry["chidro"].layout == "fixed-width"
    assert registry["chidro"].status == "schema-documented"
    installed = next(field for field in registry["chidro"].fields if field.key == "potencia_instalada")
    assert (installed.position_start, installed.position_end) == (44, 50)
    assert installed.status == "validated"
    assert payload["ctermi"]["documentation_source"] == "20250207_Diccionario_SDDP_PLEXOS_v0.xlsx"


def test_chidro_positions_match_real_fixtures() -> None:
    fixtures = (
        (Path("data/PA_202503_R25_1050_Gatun_en_BC02/chidropa.dat"), "PA-RP-490", 14.3),
        (Path("data/PE_BC/chidrope.dat"), "Huanchor", 19.6),
        (Path("data/RD_Tomas/BC01/chidrodo.dat"), "P_HYDROS_S", None),
    )
    for path, name, expected in fixtures:
        line = next(line for line in path.read_text(encoding="latin-1").splitlines() if name in line)
        assert _fixed_int(line, 34, 37) is not None
        if expected is not None:
            assert _fixed_number(line, 44, 50) == expected
