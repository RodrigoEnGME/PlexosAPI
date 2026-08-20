"""Background calculations for revision-scoped input profile summaries."""

from datetime import UTC, datetime
from statistics import mean, pstdev
from threading import Thread

from sqlalchemy import delete, select

from app.db import SessionLocal
from app.models import (
    EnergyAsset,
    StudyAnalyticsJob,
    StudyHydroDetail,
    StudyHydroInflow,
    StudyProfileStatistic,
    StudyRenewableAssignment,
    StudyRenewableHourlyProfile,
)


def recover_analytics_jobs() -> None:
    """Resume jobs left pending/running after a process restart."""
    db = SessionLocal()
    try:
        jobs = [
            job for job in db.scalars(select(StudyAnalyticsJob).where(StudyAnalyticsJob.status.in_({"pending", "running"})))
            if job.status == "pending" or job.started_at is not None
        ]
        job_ids = []
        for job in jobs:
            job.status = "pending"
            job.phase = "queued"
            job.progress = 0
            job.processed_assets = 0
            job.error_message = None
            job_ids.append(job.id)
        db.commit()
    finally:
        db.close()
    for job_id in job_ids:
        Thread(target=run_analytics_job, args=(job_id,), daemon=True).start()


def _stats(values: list[float]) -> dict[str, float | int]:
    ordered = sorted(values)
    def percentile(fraction: float) -> float:
        position = (len(ordered) - 1) * fraction
        lower = int(position)
        upper = min(lower + 1, len(ordered) - 1)
        return ordered[lower] + (ordered[upper] - ordered[lower]) * (position - lower)
    return {
        "mean": mean(values), "p10": percentile(.1), "p90": percentile(.9),
        "minimum": ordered[0], "maximum": ordered[-1],
        "standard_deviation": pstdev(values), "valid_count": len(values),
    }


def _stat_rows(asset_id: int, revision_id: int, kind: str, grouping: str, buckets: dict[int, list[float]], unit: str, source_file: str | None) -> list[dict[str, object]]:
    return [{"revision_id": revision_id, "asset_id": asset_id, "profile_kind": kind, "grouping": grouping, "bucket": bucket, "unit_name": unit, "source_file": source_file, "calculated_at": datetime.now(UTC), **_stats(values)} for bucket, values in sorted(buckets.items()) if values]


def run_analytics_job(job_id: int) -> None:
    db = SessionLocal()
    try:
        job = db.get(StudyAnalyticsJob, job_id)
        if job is None:
            return
        job.status = "running"
        job.phase = "profile statistics"
        job.started_at = datetime.now(UTC)
        db.commit()
        assignments = list(db.scalars(select(StudyRenewableAssignment).where(StudyRenewableAssignment.revision_id == job.revision_id)))
        hydro_assets = list(db.execute(select(EnergyAsset.id, StudyHydroDetail.station_code, StudyHydroDetail.source_file).join(StudyHydroDetail, (StudyHydroDetail.revision_id == EnergyAsset.revision_id) & (StudyHydroDetail.source_code == EnergyAsset.source_code)).where(EnergyAsset.revision_id == job.revision_id, EnergyAsset.asset_type == "hydro")).all())
        total = len(assignments) + len(hydro_assets)
        job.total_assets = total
        db.commit()
        db.execute(delete(StudyProfileStatistic).where(StudyProfileStatistic.revision_id == job.revision_id))
        db.commit()
        processed = 0
        for assignment in assignments:
            rows = db.execute(select(StudyRenewableHourlyProfile.hour, StudyRenewableHourlyProfile.value_pu).where(StudyRenewableHourlyProfile.revision_id == job.revision_id, StudyRenewableHourlyProfile.source_code == assignment.profile_code)).all()
            buckets: dict[int, list[float]] = {}
            for hour, value in rows:
                buckets.setdefault(((hour - 1) % 24) + 1, []).append(value)
            db.bulk_insert_mappings(StudyProfileStatistic, _stat_rows(assignment.asset_id, job.revision_id, "renewable-daily", "hour-of-day", buckets, "p.u.", assignment.source_file))
            processed += 1
            job.processed_assets = processed
            job.progress = int(processed * 100 / max(total, 1))
            db.commit()
        for asset_id, station_code, source_file in hydro_assets:
            rows = db.execute(select(StudyHydroInflow.month, StudyHydroInflow.value_m3s).where(StudyHydroInflow.revision_id == job.revision_id, StudyHydroInflow.station_code == str(station_code), StudyHydroInflow.is_missing.is_(False))).all()
            buckets: dict[int, list[float]] = {}
            for month, value in rows:
                if value is not None:
                    buckets.setdefault(month, []).append(value)
            db.bulk_insert_mappings(StudyProfileStatistic, _stat_rows(asset_id, job.revision_id, "hydro-monthly", "month-of-year", buckets, "m3/s", source_file))
            processed += 1
            job.processed_assets = processed
            job.progress = int(processed * 100 / max(total, 1))
            db.commit()
        job.status = "ready"
        job.phase = "complete"
        job.progress = 100
        job.completed_at = datetime.now(UTC)
        db.commit()
    except Exception as exc:  # noqa: BLE001
        db.rollback()
        job = db.get(StudyAnalyticsJob, job_id)
        if job:
            job.status = "failed"
            job.phase = "error"
            job.error_message = str(exc)
            job.completed_at = datetime.now(UTC)
            db.commit()
    finally:
        db.close()
