import platform
import socket
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from datetime import UTC, datetime

from fastapi import FastAPI, HTTPException, status

from forge.config import Settings
from forge.logging_config import configure_logging, get_logger
from forge.schemas import (
    CurrentMetricsResponse,
    ErrorResponse,
    HealthResponse,
    SystemInfoResponse,
)
from forge.system_metrics import MetricsCollectionError, collect_current_metrics

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


@app.get(
    "/metrics/current",
    response_model=CurrentMetricsResponse,
    responses={
        status.HTTP_503_SERVICE_UNAVAILABLE: {
            "model": ErrorResponse,
            "description": "System metrics are temporarily unavailable",
        }
    },
)
def read_current_metrics() -> CurrentMetricsResponse:
    try:
        return collect_current_metrics()
    except MetricsCollectionError as error:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Current system metrics are temporarily unavailable",
        ) from error
