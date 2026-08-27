from datetime import datetime

from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    status: str


class SystemInfoResponse(BaseModel):
    hostname: str
    operating_system: str
    python_version: str
    collected_at: datetime


class CurrentMetricsResponse(BaseModel):
    cpu_percent: float = Field(ge=0, le=100)
    memory_percent: float = Field(ge=0, le=100)
    disk_percent: float = Field(ge=0, le=100)
    collected_at: datetime


class ErrorResponse(BaseModel):
    detail: str
