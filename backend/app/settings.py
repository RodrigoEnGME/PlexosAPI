from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "SDDP a PLEXOS Converter"
    database_url: str = "sqlite:///./data/converter.db"
    cors_origins: list[str] = ["http://localhost:5173"]
    plexos_api_path: str | None = None
    plexos_engine_path: str | None = None
    dataset_root: str = "data/UY_SDDP"
    artifact_root: str = "data/artifacts"
    max_upload_bytes: int = 2_000_000_000
    max_archive_entries: int = 100_000
    max_archive_uncompressed_bytes: int = 10_000_000_000

    model_config = SettingsConfigDict(env_file=".env", env_prefix="CONVERTER_", extra="ignore")


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
