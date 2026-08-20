from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Index, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db import Base


class Tenant(Base):
    __tablename__ = "tenants"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), unique=True, index=True)
    code: Mapped[str] = mapped_column(String(40), unique=True, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    projects: Mapped[list["Project"]] = relationship(back_populates="tenant")


class Project(Base):
    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(primary_key=True)
    tenant_id: Mapped[int] = mapped_column(ForeignKey("tenants.id"), index=True)
    name: Mapped[str] = mapped_column(String(160))
    source_system: Mapped[str] = mapped_column(String(40), default="SDDP")
    target_system: Mapped[str] = mapped_column(String(40), default="PLEXOS 9")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    tenant: Mapped[Tenant] = relationship(back_populates="projects")
    conversions: Mapped[list["Conversion"]] = relationship(back_populates="project")
    revisions: Mapped[list["StudyRevision"]] = relationship(back_populates="project")


class Conversion(Base):
    __tablename__ = "conversions"

    id: Mapped[int] = mapped_column(primary_key=True)
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"), index=True)
    status: Mapped[str] = mapped_column(String(30), default="pending")
    source_filename: Mapped[str] = mapped_column(String(255))
    detected_encoding: Mapped[str | None] = mapped_column(String(40), nullable=True)
    diagnostics: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    project: Mapped[Project] = relationship(back_populates="conversions")


class DatasetFile(Base):
    __tablename__ = "dataset_files"

    id: Mapped[int] = mapped_column(primary_key=True)
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"), index=True)
    revision_id: Mapped[int | None] = mapped_column(ForeignKey("study_revisions.id"), nullable=True, index=True)
    relative_path: Mapped[str] = mapped_column(String(500), index=True)
    extension: Mapped[str] = mapped_column(String(20), index=True)
    size_bytes: Mapped[int] = mapped_column(Integer)
    sha256: Mapped[str] = mapped_column(String(64), index=True)
    file_kind: Mapped[str] = mapped_column(String(30))
    encoding: Mapped[str | None] = mapped_column(String(40), nullable=True)
    line_count: Mapped[int] = mapped_column(Integer, default=0)
    record_count: Mapped[int] = mapped_column(Integer, default=0)
    parse_status: Mapped[str] = mapped_column(String(30), default="discovered")
    parse_message: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    records: Mapped[list["DatasetRecord"]] = relationship(
        back_populates="file", cascade="all, delete-orphan"
    )


class DatasetRecord(Base):
    __tablename__ = "dataset_records"

    id: Mapped[int] = mapped_column(primary_key=True)
    file_id: Mapped[int] = mapped_column(ForeignKey("dataset_files.id"), index=True)
    line_number: Mapped[int] = mapped_column(Integer)
    section: Mapped[str | None] = mapped_column(String(160), nullable=True)
    raw_text: Mapped[str] = mapped_column(Text)
    tokens_json: Mapped[str] = mapped_column(Text)
    record_kind: Mapped[str] = mapped_column(String(30), default="data")
    file: Mapped[DatasetFile] = relationship(back_populates="records")


class StudyDescriptor(Base):
    __tablename__ = "study_descriptors"

    id: Mapped[int] = mapped_column(primary_key=True)
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"), index=True)
    revision_id: Mapped[int | None] = mapped_column(ForeignKey("study_revisions.id"), nullable=True, index=True)
    source_file: Mapped[str] = mapped_column(String(255))
    parser_version: Mapped[str] = mapped_column(String(30), default="sddp-17.2-initial")
    descriptor_json: Mapped[str] = mapped_column(Text)
    warnings_json: Mapped[str] = mapped_column(Text, default="[]")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class ImportRun(Base):
    __tablename__ = "import_runs"

    id: Mapped[int] = mapped_column(primary_key=True)
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"), index=True)
    source_path: Mapped[str] = mapped_column(String(500))
    status: Mapped[str] = mapped_column(String(30), default="running")
    files_total: Mapped[int] = mapped_column(Integer, default=0)
    files_processed: Mapped[int] = mapped_column(Integer, default=0)
    files_binary: Mapped[int] = mapped_column(Integer, default=0)
    errors: Mapped[int] = mapped_column(Integer, default=0)
    message: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    revision: Mapped["StudyRevision | None"] = relationship(back_populates="import_run")


class StudyRevision(Base):
    __tablename__ = "study_revisions"

    id: Mapped[int] = mapped_column(primary_key=True)
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"), index=True)
    import_run_id: Mapped[int | None] = mapped_column(ForeignKey("import_runs.id"), nullable=True)
    revision_number: Mapped[int] = mapped_column(Integer)
    status: Mapped[str] = mapped_column(String(30), default="draft")
    source_archive_uri: Mapped[str | None] = mapped_column(String(1000), nullable=True)
    source_archive_sha256: Mapped[str | None] = mapped_column(String(64), nullable=True)
    is_active: Mapped[bool] = mapped_column(default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    project: Mapped[Project] = relationship(back_populates="revisions")
    import_run: Mapped[ImportRun | None] = relationship(back_populates="revision")
    systems: Mapped[list["StudySystem"]] = relationship(back_populates="revision", cascade="all, delete-orphan")
    assets: Mapped[list["EnergyAsset"]] = relationship(back_populates="revision", cascade="all, delete-orphan")
    modifications: Mapped[list["AssetModification"]] = relationship(back_populates="revision", cascade="all, delete-orphan")


class StudySystem(Base):
    __tablename__ = "study_systems"

    id: Mapped[int] = mapped_column(primary_key=True)
    revision_id: Mapped[int] = mapped_column(ForeignKey("study_revisions.id"), index=True)
    code: Mapped[str] = mapped_column(String(40))
    name: Mapped[str] = mapped_column(String(160))
    country_code: Mapped[str | None] = mapped_column(String(10), nullable=True)
    revision: Mapped[StudyRevision] = relationship(back_populates="systems")
    buses: Mapped[list["StudyBus"]] = relationship(back_populates="system", cascade="all, delete-orphan")


class StudyBus(Base):
    __tablename__ = "study_buses"

    id: Mapped[int] = mapped_column(primary_key=True)
    revision_id: Mapped[int] = mapped_column(ForeignKey("study_revisions.id"), index=True)
    system_id: Mapped[int | None] = mapped_column(ForeignKey("study_systems.id"), nullable=True)
    source_code: Mapped[str] = mapped_column(String(40), index=True)
    name: Mapped[str] = mapped_column(String(160))
    latitude: Mapped[float | None] = mapped_column(nullable=True)
    longitude: Mapped[float | None] = mapped_column(nullable=True)
    coordinate_source: Mapped[str | None] = mapped_column(String(255), nullable=True)
    nominal_voltage_kv: Mapped[float | None] = mapped_column(nullable=True)
    demand_block_mw_json: Mapped[str] = mapped_column(Text, default="{}")
    source_file: Mapped[str | None] = mapped_column(String(255), nullable=True)
    source_line: Mapped[int | None] = mapped_column(Integer, nullable=True)
    system: Mapped[StudySystem | None] = relationship(back_populates="buses")


class StudyDemand(Base):
    __tablename__ = "study_demands"

    id: Mapped[int] = mapped_column(primary_key=True)
    revision_id: Mapped[int] = mapped_column(ForeignKey("study_revisions.id"), index=True)
    system_id: Mapped[int | None] = mapped_column(ForeignKey("study_systems.id"), nullable=True, index=True)
    source_code: Mapped[str] = mapped_column(String(40), index=True)
    segment: Mapped[int] = mapped_column(Integer, default=1)
    year: Mapped[int] = mapped_column(Integer, index=True)
    block: Mapped[int] = mapped_column(Integer, index=True)
    monthly_gwh_json: Mapped[str] = mapped_column(Text)
    source_file: Mapped[str] = mapped_column(String(255))
    source_line: Mapped[int] = mapped_column(Integer)


class StudyDemandDefinition(Base):
    __tablename__ = "study_demand_definitions"

    id: Mapped[int] = mapped_column(primary_key=True)
    revision_id: Mapped[int] = mapped_column(ForeignKey("study_revisions.id"), index=True)
    system_id: Mapped[int | None] = mapped_column(ForeignKey("study_systems.id"), nullable=True, index=True)
    source_code: Mapped[str] = mapped_column(String(40), index=True)
    name: Mapped[str] = mapped_column(String(160))
    segment_count: Mapped[int] = mapped_column(Integer, default=0)
    first_segment_type: Mapped[int | None] = mapped_column(Integer, nullable=True)
    source_file: Mapped[str] = mapped_column(String(255))
    source_line: Mapped[int] = mapped_column(Integer)


class StudyFuel(Base):
    __tablename__ = "study_fuels"

    id: Mapped[int] = mapped_column(primary_key=True)
    revision_id: Mapped[int] = mapped_column(ForeignKey("study_revisions.id"), index=True)
    system_id: Mapped[int | None] = mapped_column(ForeignKey("study_systems.id"), nullable=True, index=True)
    source_code: Mapped[str] = mapped_column(String(40), index=True)
    name: Mapped[str] = mapped_column(String(160))
    unit_name: Mapped[str | None] = mapped_column(String(40), nullable=True)
    base_cost: Mapped[float | None] = mapped_column(nullable=True)
    co2_factor: Mapped[float | None] = mapped_column(nullable=True)
    source_file: Mapped[str] = mapped_column(String(255))
    source_line: Mapped[int] = mapped_column(Integer)


class StudyFuelPrice(Base):
    __tablename__ = "study_fuel_prices"

    id: Mapped[int] = mapped_column(primary_key=True)
    revision_id: Mapped[int] = mapped_column(ForeignKey("study_revisions.id"), index=True)
    fuel_code: Mapped[str] = mapped_column(String(40), index=True)
    year: Mapped[int] = mapped_column(Integer, index=True)
    month: Mapped[int] = mapped_column(Integer, index=True)
    price: Mapped[float] = mapped_column()
    source_file: Mapped[str] = mapped_column(String(255))
    source_line: Mapped[int] = mapped_column(Integer)


class StudyCurrency(Base):
    __tablename__ = "study_currencies"

    id: Mapped[int] = mapped_column(primary_key=True)
    revision_id: Mapped[int] = mapped_column(ForeignKey("study_revisions.id"), index=True)
    code: Mapped[str] = mapped_column(String(12), index=True)
    conversion_to_reference: Mapped[float] = mapped_column()
    is_reference: Mapped[bool] = mapped_column(default=False)
    source_file: Mapped[str] = mapped_column(String(255))
    source_line: Mapped[int] = mapped_column(Integer)


class StudyBusDemand(Base):
    __tablename__ = "study_bus_demands"

    id: Mapped[int] = mapped_column(primary_key=True)
    revision_id: Mapped[int] = mapped_column(ForeignKey("study_revisions.id"), index=True)
    bus_code: Mapped[str] = mapped_column(String(40), index=True)
    demand_code: Mapped[str] = mapped_column(String(40), index=True)
    effective_date: Mapped[datetime] = mapped_column(DateTime, index=True)
    block: Mapped[int] = mapped_column(Integer, index=True)
    demand_mw: Mapped[float] = mapped_column()
    source_file: Mapped[str] = mapped_column(String(255))
    source_line: Mapped[int] = mapped_column(Integer)


class StudyLoadLevelMap(Base):
    __tablename__ = "study_load_level_maps"

    id: Mapped[int] = mapped_column(primary_key=True)
    revision_id: Mapped[int] = mapped_column(ForeignKey("study_revisions.id"), index=True)
    year: Mapped[int] = mapped_column(Integer, index=True)
    month: Mapped[int] = mapped_column(Integer, index=True)
    hour: Mapped[int] = mapped_column(Integer, index=True)
    load_level: Mapped[int] = mapped_column(Integer, index=True)
    source_file: Mapped[str] = mapped_column(String(255))
    source_line: Mapped[int] = mapped_column(Integer)
    __table_args__ = (UniqueConstraint("revision_id", "month", "hour", name="uq_load_level_map_hour"),)


class StudyHourlyLoad(Base):
    __tablename__ = "study_hourly_loads"

    id: Mapped[int] = mapped_column(primary_key=True)
    revision_id: Mapped[int] = mapped_column(ForeignKey("study_revisions.id"), index=True)
    load_code: Mapped[str] = mapped_column(String(160), index=True)
    year: Mapped[int] = mapped_column(Integer, index=True)
    month: Mapped[int] = mapped_column(Integer, index=True)
    hour: Mapped[int] = mapped_column(Integer, index=True)
    value_mw: Mapped[float] = mapped_column()
    source_file: Mapped[str] = mapped_column(String(255))
    source_line: Mapped[int] = mapped_column(Integer)
    __table_args__ = (Index("ix_hourly_load_revision_code_year_month_hour", "revision_id", "load_code", "year", "month", "hour"),)


class StudyCircuit(Base):
    __tablename__ = "study_circuits"

    id: Mapped[int] = mapped_column(primary_key=True)
    revision_id: Mapped[int] = mapped_column(ForeignKey("study_revisions.id"), index=True)
    source_code: Mapped[str] = mapped_column(String(40), index=True)
    from_bus: Mapped[str] = mapped_column(String(40))
    to_bus: Mapped[str] = mapped_column(String(40))
    name: Mapped[str] = mapped_column(String(160))
    normal_limit_mw: Mapped[float | None] = mapped_column(nullable=True)
    emergency_limit_mw: Mapped[float | None] = mapped_column(nullable=True)
    status: Mapped[str] = mapped_column(String(30), default="connected")
    nominal_voltage_kv: Mapped[float | None] = mapped_column(nullable=True)
    voltage_source: Mapped[str | None] = mapped_column(String(80), nullable=True)
    source_file: Mapped[str | None] = mapped_column(String(255), nullable=True)
    source_line: Mapped[int | None] = mapped_column(Integer, nullable=True)


class EnergyAsset(Base):
    __tablename__ = "energy_assets"

    id: Mapped[int] = mapped_column(primary_key=True)
    revision_id: Mapped[int] = mapped_column(ForeignKey("study_revisions.id"), index=True)
    system_id: Mapped[int | None] = mapped_column(ForeignKey("study_systems.id"), nullable=True)
    bus_code: Mapped[str | None] = mapped_column(String(40), nullable=True, index=True)
    source_code: Mapped[str] = mapped_column(String(40), index=True)
    name: Mapped[str] = mapped_column(String(160))
    asset_type: Mapped[str] = mapped_column(String(40))
    technology: Mapped[str | None] = mapped_column(String(40), nullable=True)
    capacity_mw: Mapped[float | None] = mapped_column(nullable=True)
    operating_factor: Mapped[float | None] = mapped_column(nullable=True)
    lifecycle_status: Mapped[str] = mapped_column(String(30), default="existing")
    source_file: Mapped[str] = mapped_column(String(255))
    source_line: Mapped[int] = mapped_column(Integer)
    revision: Mapped[StudyRevision] = relationship(back_populates="assets")


class StudyThermalDetail(Base):
    __tablename__ = "study_thermal_details"

    id: Mapped[int] = mapped_column(primary_key=True)
    revision_id: Mapped[int] = mapped_column(ForeignKey("study_revisions.id"), index=True)
    source_code: Mapped[str] = mapped_column(String(40), index=True)
    unit_count: Mapped[int | None] = mapped_column(Integer, nullable=True)
    plant_type: Mapped[int | None] = mapped_column(Integer, nullable=True)
    min_generation_mw: Mapped[float | None] = mapped_column(nullable=True)
    max_generation_mw: Mapped[float | None] = mapped_column(nullable=True)
    short_term_outage_pct: Mapped[float | None] = mapped_column(nullable=True)
    historical_outage_pct: Mapped[float | None] = mapped_column(nullable=True)
    variable_om_cost: Mapped[float | None] = mapped_column(nullable=True)
    fuel_code: Mapped[str | None] = mapped_column(String(40), nullable=True, index=True)
    consumption_segments_json: Mapped[str] = mapped_column(Text, default="[]")
    alternative_fuels_json: Mapped[str] = mapped_column(Text, default="[]")
    commitment_type: Mapped[int | None] = mapped_column(Integer, nullable=True)
    transport_cost: Mapped[float | None] = mapped_column(nullable=True)
    startup_cost: Mapped[float | None] = mapped_column(nullable=True)
    gas_system: Mapped[int | None] = mapped_column(Integer, nullable=True)
    combined_cycle_code: Mapped[int | None] = mapped_column(Integer, nullable=True)
    emission_factor: Mapped[float | None] = mapped_column(nullable=True)
    source_file: Mapped[str] = mapped_column(String(255))
    source_line: Mapped[int] = mapped_column(Integer)


class StudyHydroDetail(Base):
    __tablename__ = "study_hydro_details"

    id: Mapped[int] = mapped_column(primary_key=True)
    revision_id: Mapped[int] = mapped_column(ForeignKey("study_revisions.id"), index=True)
    source_code: Mapped[str] = mapped_column(String(40), index=True)
    station_code: Mapped[int | None] = mapped_column(Integer, nullable=True)
    downstream_spill_code: Mapped[int | None] = mapped_column(Integer, nullable=True)
    downstream_turbine_code: Mapped[int | None] = mapped_column(Integer, nullable=True)
    unit_count: Mapped[int | None] = mapped_column(Integer, nullable=True)
    plant_type: Mapped[int | None] = mapped_column(Integer, nullable=True)
    production_factor: Mapped[float | None] = mapped_column(nullable=True)
    min_turbine_flow: Mapped[float | None] = mapped_column(nullable=True)
    max_turbine_flow: Mapped[float | None] = mapped_column(nullable=True)
    min_volume_hm3: Mapped[float | None] = mapped_column(nullable=True)
    max_volume_hm3: Mapped[float | None] = mapped_column(nullable=True)
    initial_condition: Mapped[float | None] = mapped_column(nullable=True)
    min_total_flow: Mapped[float | None] = mapped_column(nullable=True)
    spill_mode: Mapped[int | None] = mapped_column(Integer, nullable=True)
    short_term_outage_pct: Mapped[float | None] = mapped_column(nullable=True)
    historical_outage_pct: Mapped[float | None] = mapped_column(nullable=True)
    production_curve_json: Mapped[str] = mapped_column(Text, default="[]")
    level_volume_curve_json: Mapped[str] = mapped_column(Text, default="[]")
    source_file: Mapped[str] = mapped_column(String(255))
    source_line: Mapped[int] = mapped_column(Integer)


class StudyRenewableDetail(Base):
    __tablename__ = "study_renewable_details"

    id: Mapped[int] = mapped_column(primary_key=True)
    revision_id: Mapped[int] = mapped_column(ForeignKey("study_revisions.id"), index=True)
    source_code: Mapped[str] = mapped_column(String(40), index=True)
    unit_count: Mapped[int | None] = mapped_column(Integer, nullable=True)
    plant_type: Mapped[int | None] = mapped_column(Integer, nullable=True)
    operating_factor: Mapped[float | None] = mapped_column(nullable=True)
    failure_probability: Mapped[float | None] = mapped_column(nullable=True)
    technology_type: Mapped[int | None] = mapped_column(Integer, nullable=True)
    source_file: Mapped[str] = mapped_column(String(255))
    source_line: Mapped[int] = mapped_column(Integer)


class StudyRenewableProfile(Base):
    __tablename__ = "study_renewable_profiles"

    id: Mapped[int] = mapped_column(primary_key=True)
    revision_id: Mapped[int] = mapped_column(ForeignKey("study_revisions.id"), index=True)
    source_code: Mapped[str] = mapped_column(String(40), index=True)
    stage: Mapped[int] = mapped_column(Integer, index=True)
    scenario: Mapped[int] = mapped_column(Integer, index=True)
    block: Mapped[int] = mapped_column(Integer, index=True)
    value_pu: Mapped[float] = mapped_column()
    source_file: Mapped[str] = mapped_column(String(255))
    source_line: Mapped[int] = mapped_column(Integer)


class StudyRenewableHourlyProfile(Base):
    __tablename__ = "study_renewable_hourly_profiles"

    id: Mapped[int] = mapped_column(primary_key=True)
    revision_id: Mapped[int] = mapped_column(ForeignKey("study_revisions.id"), index=True)
    source_code: Mapped[str] = mapped_column(String(160), index=True)
    scenario: Mapped[int] = mapped_column(Integer, index=True)
    year: Mapped[int] = mapped_column(Integer, index=True)
    month: Mapped[int] = mapped_column(Integer, index=True)
    hour: Mapped[int] = mapped_column(Integer, index=True)
    value_pu: Mapped[float] = mapped_column()
    source_file: Mapped[str] = mapped_column(String(255))
    source_line: Mapped[int] = mapped_column(Integer)
    __table_args__ = (Index("ix_renewable_hourly_revision_source_month_scenario_hour", "revision_id", "source_code", "month", "scenario", "hour"),)


class StudyRenewableAssignment(Base):
    __tablename__ = "study_renewable_assignments"

    id: Mapped[int] = mapped_column(primary_key=True)
    revision_id: Mapped[int] = mapped_column(ForeignKey("study_revisions.id"), index=True)
    asset_id: Mapped[int] = mapped_column(ForeignKey("energy_assets.id"), index=True)
    site_code: Mapped[str] = mapped_column(String(40), index=True)
    profile_code: Mapped[str] = mapped_column(String(160), index=True)
    technology_type: Mapped[int | None] = mapped_column(Integer, nullable=True)
    source_file: Mapped[str] = mapped_column(String(255))
    source_line: Mapped[int] = mapped_column(Integer)
    __table_args__ = (Index("ix_renewable_assignment_revision_asset", "revision_id", "asset_id"),)


class StudyHydroStation(Base):
    __tablename__ = "study_hydro_stations"

    id: Mapped[int] = mapped_column(primary_key=True)
    revision_id: Mapped[int] = mapped_column(ForeignKey("study_revisions.id"), index=True)
    source_code: Mapped[str] = mapped_column(String(40), index=True)
    name: Mapped[str] = mapped_column(String(160))
    downstream_code: Mapped[str | None] = mapped_column(String(40), nullable=True)
    incremental_null: Mapped[bool] = mapped_column(default=False)
    source_file: Mapped[str] = mapped_column(String(255))
    source_line: Mapped[int] = mapped_column(Integer)


class StudyHydroInflow(Base):
    __tablename__ = "study_hydro_inflows"

    id: Mapped[int] = mapped_column(primary_key=True)
    revision_id: Mapped[int] = mapped_column(ForeignKey("study_revisions.id"), index=True)
    station_code: Mapped[str] = mapped_column(String(40), index=True)
    month: Mapped[int] = mapped_column(Integer, index=True)
    year: Mapped[int] = mapped_column(Integer, index=True)
    value_m3s: Mapped[float | None] = mapped_column(nullable=True)
    is_missing: Mapped[bool] = mapped_column(default=False)
    source_file: Mapped[str] = mapped_column(String(255))
    source_line: Mapped[int] = mapped_column(Integer)
    __table_args__ = (Index("ix_hydro_inflow_revision_station_missing_month", "revision_id", "station_code", "is_missing", "month"),)


class StudyProfileStatistic(Base):
    __tablename__ = "study_profile_statistics"

    id: Mapped[int] = mapped_column(primary_key=True)
    revision_id: Mapped[int] = mapped_column(ForeignKey("study_revisions.id"), index=True)
    asset_id: Mapped[int] = mapped_column(ForeignKey("energy_assets.id"), index=True)
    profile_kind: Mapped[str] = mapped_column(String(40), index=True)
    grouping: Mapped[str] = mapped_column(String(40))
    bucket: Mapped[int] = mapped_column(Integer)
    mean: Mapped[float] = mapped_column()
    p10: Mapped[float] = mapped_column()
    p90: Mapped[float] = mapped_column()
    minimum: Mapped[float] = mapped_column()
    maximum: Mapped[float] = mapped_column()
    standard_deviation: Mapped[float] = mapped_column()
    valid_count: Mapped[int] = mapped_column(Integer)
    unit_name: Mapped[str] = mapped_column(String(20))
    source_file: Mapped[str | None] = mapped_column(String(255), nullable=True)
    calculated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    __table_args__ = (UniqueConstraint("revision_id", "asset_id", "profile_kind", "grouping", "bucket", name="uq_profile_statistic_bucket"),)


class StudyAnalyticsJob(Base):
    __tablename__ = "study_analytics_jobs"

    id: Mapped[int] = mapped_column(primary_key=True)
    revision_id: Mapped[int] = mapped_column(ForeignKey("study_revisions.id"), unique=True, index=True)
    status: Mapped[str] = mapped_column(String(20), default="pending")
    phase: Mapped[str] = mapped_column(String(60), default="queued")
    total_assets: Mapped[int] = mapped_column(Integer, default=0)
    processed_assets: Mapped[int] = mapped_column(Integer, default=0)
    progress: Mapped[int] = mapped_column(Integer, default=0)
    error_message: Mapped[str | None] = mapped_column(Text, nullable=True)
    started_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)


class AssetModification(Base):
    __tablename__ = "asset_modifications"

    id: Mapped[int] = mapped_column(primary_key=True)
    revision_id: Mapped[int] = mapped_column(ForeignKey("study_revisions.id"), index=True)
    entity_type: Mapped[str] = mapped_column(String(40))
    source_code: Mapped[str] = mapped_column(String(40), index=True)
    effective_date: Mapped[datetime] = mapped_column(DateTime, index=True)
    effective_stage: Mapped[int | None] = mapped_column(Integer, nullable=True)
    effective_block: Mapped[int | None] = mapped_column(Integer, nullable=True)
    changed_fields_json: Mapped[str] = mapped_column(Text)
    source_file: Mapped[str] = mapped_column(String(255))
    source_line: Mapped[int] = mapped_column(Integer)
    sequence: Mapped[int] = mapped_column(Integer, default=0)
    revision: Mapped[StudyRevision] = relationship(back_populates="modifications")


class StudyMaintenance(Base):
    __tablename__ = "study_maintenances"

    id: Mapped[int] = mapped_column(primary_key=True)
    revision_id: Mapped[int] = mapped_column(ForeignKey("study_revisions.id"), index=True)
    asset_type: Mapped[str] = mapped_column(String(20))
    source_code: Mapped[str] = mapped_column(String(40), index=True)
    asset_name: Mapped[str] = mapped_column(String(160))
    measure_type: Mapped[int] = mapped_column(Integer)
    unit_type: Mapped[int] = mapped_column(Integer)
    year: Mapped[int] = mapped_column(Integer, index=True)
    stage_values_json: Mapped[str] = mapped_column(Text)
    source_file: Mapped[str] = mapped_column(String(255))
    source_line: Mapped[int] = mapped_column(Integer)
    warnings_json: Mapped[str] = mapped_column(Text, default="[]")
