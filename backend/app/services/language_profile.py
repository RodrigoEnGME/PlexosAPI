"""Language-aware aliases for SDDP headers and block labels."""

import re
import unicodedata

LANGUAGE_NAMES = {0: "en", 1: "es", 2: "pt"}

ALIASES: dict[str, dict[str, tuple[str, ...]]] = {
    "plant_name": {"en": ("name",), "es": ("nombre",), "pt": ("nome",)},
    "plant": {"en": ("plant",), "es": ("planta",), "pt": ("usina", "planta")},
    "load": {"en": ("load",), "es": ("carga",), "pt": ("carga",)},
    "fuel": {"en": ("fuel",), "es": ("combustible",), "pt": ("combustivel",)},
    "info_type": {"en": ("info type",), "es": ("tipo info",), "pt": ("tipo info",)},
    "units": {"en": ("units",), "es": ("unidades",), "pt": ("unidades",)},
}


def language_code(value: int | str | None) -> str:
    try:
        return LANGUAGE_NAMES.get(int(value), "es")
    except (TypeError, ValueError):
        return "es"


def normalize_label(value: str | None) -> str:
    text = unicodedata.normalize("NFKD", value or "")
    text = "".join(character for character in text if not unicodedata.combining(character))
    text = re.sub(r"[^a-zA-Z0-9]+", " ", text.casefold())
    return " ".join(text.split())


def canonical_label(value: str | None, language: int | str | None = None) -> str | None:
    normalized = normalize_label(value)
    if not normalized:
        return None
    preferred = language_code(language)
    for canonical, profiles in ALIASES.items():
        aliases = profiles.get(preferred, ()) + tuple(
            alias for code, values in profiles.items() if code != preferred for alias in values
        )
        if normalized in {normalize_label(alias) for alias in aliases}:
            return canonical
    return None


def localized_marker_pattern(canonical: str, language: int | str | None = None) -> str:
    """Return an escaped pattern for a localized block marker."""
    preferred = language_code(language)
    aliases = ALIASES[canonical].get(preferred, ()) + tuple(
        alias for code, values in ALIASES[canonical].items() if code != preferred for alias in values
    )
    return "(?:" + "|".join(re.escape(alias).replace(r"\ ", r"\s+") for alias in aliases) + ")"
