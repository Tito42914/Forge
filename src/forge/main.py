import platform
import socket
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from datetime import UTC, datetime
from pathlib import Path

import psutil
from fastapi import FastAPI

from forge.config import Settings
from forge.logging_config import configure_logging, get_logger
from forge.schemas import CurrentMetricsResponse, HealthResponse, SystemInfoResponse

settings = Settings()
configure_logging(settings.log_level)
logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    logger.info(
        "%s %s starting in the %s environment",
        settings.app_name,
        settings.app_version,
        settings.environment,
    )

    yield

    logger.info("%s stopping", settings.app_name)


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    lifespan=lifespan,
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
