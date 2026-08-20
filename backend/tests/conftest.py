"""Keep destructive schema-reset fixtures away from the operator database."""

import os

import pytest

os.environ.setdefault("CONVERTER_DATABASE_URL", "sqlite:///./data/test-converter.db")


@pytest.fixture(scope="session", autouse=True)
def reset_isolated_test_database():
    from app.db import Base, engine, init_db

    init_db()
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    yield
