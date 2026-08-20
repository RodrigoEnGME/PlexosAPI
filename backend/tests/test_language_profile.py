import re

import pytest

from app.services.language_profile import (
    canonical_label,
    language_code,
    localized_marker_pattern,
    normalize_label,
)


@pytest.mark.parametrize(
    ("value", "language", "expected"),
    [
        ("Name........", 0, "plant_name"),
        ("Nombre.....", 1, "plant_name"),
        ("Nome........", 2, "plant_name"),
        ("Combustível", 2, "fuel"),
        ("Tipo Info.", 1, "info_type"),
    ],
)
def test_canonicalizes_localized_labels(value: str, language: int, expected: str) -> None:
    assert canonical_label(value, language) == expected


def test_language_code_defaults_safely() -> None:
    assert language_code(0) == "en"
    assert language_code(1) == "es"
    assert language_code(2) == "pt"
    assert language_code(99) == "es"
    assert normalize_label("  Nombre... ") == "nombre"


def test_localized_marker_pattern_matches_all_supported_languages() -> None:
    pattern = localized_marker_pattern("plant")
    assert re.search(rf"^\*\*\*\*\s*{pattern}\s*:\s*643", "**** Plant: 643 PA-RP-490", re.IGNORECASE)
    assert re.search(rf"^\*\*\*\*\s*{pattern}\s*:\s*643", "**** Planta: 643 PA-RP-490", re.IGNORECASE)
    assert re.search(rf"^\*\*\*\*\s*{pattern}\s*:\s*643", "**** Usina: 643 PA-RP-490", re.IGNORECASE)
