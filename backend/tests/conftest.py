"""Keep destructive schema-reset fixtures away from the operator database."""

import os

os.environ.setdefault("CONVERTER_DATABASE_URL", "sqlite:///./data/test-converter.db")
