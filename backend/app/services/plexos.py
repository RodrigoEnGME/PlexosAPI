from pathlib import Path

from app.settings import settings


class PlexosUnavailableError(RuntimeError):
    pass


def check_plexos9_api() -> dict[str, str | bool]:
    """Check local PLEXOS 9 API availability without importing proprietary assemblies."""
    if not settings.plexos_api_path:
        return {"available": False, "reason": "CONVERTER_PLEXOS_API_PATH is not configured"}
    path = Path(settings.plexos_api_path)
    return {"available": path.exists(), "path": str(path)}
