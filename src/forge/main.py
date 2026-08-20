import platform
import socket
from datetime import UTC, datetime
from pathlib import Path

import psutil
from fastapi import FastAPI

from forge.config import Settings
from forge.schemas import CurrentMetricsResponse, HealthResponse, SystemInfoResponse

settings = Settings()

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
)


@app.get("/health", response_model=HealthResponse)
def read_health() -> HealthResponse:
    return HealthResponse(status="healthy")


@app.get("/system", response_model=SystemInfoResponse)
def read_system_info() -> SystemInfoResponse:
    return SystemInfoResponse(
        hostname=socket.gethostname(),
        operating_system=platform.system(),
        python_version=platform.python_version(),
        collected_at=datetime.now(UTC),
    )


@app.get("/metrics/current", response_model=CurrentMetricsResponse)
def read_current_metrics() -> CurrentMetricsResponse:
    disk_root = Path.cwd().anchor

    return CurrentMetricsResponse(
        cpu_percent=psutil.cpu_percent(interval=0.1),
        memory_percent=psutil.virtual_memory().percent,
        disk_percent=psutil.disk_usage(disk_root).percent,
        collected_at=datetime.now(UTC),
    )
