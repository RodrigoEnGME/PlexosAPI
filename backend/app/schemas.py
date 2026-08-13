from datetime import datetime

from pydantic import BaseModel, ConfigDict


class TenantCreate(BaseModel):
    name: str
    code: str


class TenantRead(TenantCreate):
    id: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)


class ProjectCreate(BaseModel):
    name: str


class ProjectRead(ProjectCreate):
    id: int
    tenant_id: int
    source_system: str
    target_system: str
    model_config = ConfigDict(from_attributes=True)


class ConversionRead(BaseModel):
    id: int
    project_id: int
    status: str
    source_filename: str
    detected_encoding: str | None
    diagnostics: str | None
    model_config = ConfigDict(from_attributes=True)


class DatasetFileRead(BaseModel):
    id: int
    project_id: int
    relative_path: str
    extension: str
    size_bytes: int
    sha256: str
    file_kind: str
    encoding: str | None
    line_count: int
    record_count: int
    parse_status: str
    parse_message: str | None
    model_config = ConfigDict(from_attributes=True)


class ImportRunRead(BaseModel):
    id: int
    project_id: int
    source_path: str
    status: str
    files_total: int
    files_processed: int
    files_binary: int
    errors: int
    message: str | None
    model_config = ConfigDict(from_attributes=True)


class StudyDescriptorRead(BaseModel):
    project_id: int
    source_file: str
    parser_version: str
    descriptor_json: str
    warnings_json: str
    model_config = ConfigDict(from_attributes=True)


class StudyRevisionRead(BaseModel):
    id: int
    project_id: int
    revision_number: int
    status: str
    source_archive_uri: str | None
    source_archive_sha256: str | None
    is_active: bool
    model_config = ConfigDict(from_attributes=True)
