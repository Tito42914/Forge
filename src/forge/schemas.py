from datetime import datetime

from pydantic import BaseModel


class HealthResponse(BaseModel):
    status: str


class SystemInfoResponse(BaseModel):
    hostname: str
    operating_system: str
    python_version: str
    collected_at: datetime


class CurrentMetricsResponse(BaseModel):
    cpu_percent: float
    memory_percent: float
    disk_percent: float
    collected_at: datetime
