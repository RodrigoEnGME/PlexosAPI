from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import router
from app.db import init_db
from app.services.analytics import recover_analytics_jobs
from app.settings import settings


@asynccontextmanager
async def lifespan(_: FastAPI):
    init_db()
    recover_analytics_jobs()
    yield


app = FastAPI(
    title="SDDP a PLEXOS Converter API",
    version="0.1.0",
    description="Tenant-aware API for importing, validating and converting SDDP models.",
    lifespan=lifespan,
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(router, prefix="/api")


@app.get("/health", tags=["system"])
def health() -> dict[str, str]:
    return {"status": "ok", "service": "sddp-plexos-converter"}
