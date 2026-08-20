from collections.abc import Generator
from pathlib import Path

from sqlalchemy import create_engine, event, text
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from app.settings import settings


class Base(DeclarativeBase):
    pass


is_sqlite = settings.database_url.startswith("sqlite")
connect_args = {"check_same_thread": False, "timeout": 30} if is_sqlite else {}
engine = create_engine(settings.database_url, connect_args=connect_args, pool_pre_ping=True)

if is_sqlite:
    @event.listens_for(engine, "connect")
    def _configure_sqlite(dbapi_connection, _connection_record) -> None:
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA journal_mode=WAL")
        cursor.execute("PRAGMA busy_timeout=30000")
        cursor.execute("PRAGMA synchronous=NORMAL")
        cursor.close()
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)


def init_db() -> None:
    if settings.database_url.startswith("sqlite"):
        Path("data").mkdir(exist_ok=True)
    from app.models import (  # noqa: F401
        AssetModification,
        Conversion,
        DatasetFile,
        DatasetRecord,
        EnergyAsset,
        ImportRun,
        Project,
        StudyAnalyticsJob,
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
        StudyProfileStatistic,
        StudyRenewableAssignment,
        StudyRenewableDetail,
        StudyRenewableHourlyProfile,
        StudyRenewableProfile,
        StudyRevision,
        StudySystem,
        StudyThermalDetail,
        Tenant,
    )

    Base.metadata.create_all(bind=engine)
    with engine.begin() as connection:
        connection.execute(text("CREATE INDEX IF NOT EXISTS ix_renewable_hourly_revision_source_month_scenario_hour ON study_renewable_hourly_profiles (revision_id, source_code, month, scenario, hour)"))
        connection.execute(text("CREATE INDEX IF NOT EXISTS ix_hydro_inflow_revision_station_missing_month ON study_hydro_inflows (revision_id, station_code, is_missing, month)"))


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
