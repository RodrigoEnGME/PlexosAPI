from collections.abc import Generator
from pathlib import Path

from sqlalchemy import create_engine, event
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
        StudyBus,
        StudyBusDemand,
        StudyCircuit,
        StudyDemand,
        StudyDescriptor,
        StudyMaintenance,
        StudyRevision,
        StudySystem,
        Tenant,
    )

    Base.metadata.create_all(bind=engine)


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
