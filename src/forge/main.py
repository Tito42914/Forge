import platform
import socket
from datetime import UTC, datetime

from fastapi import FastAPI

from forge.config import Settings
from forge.schemas import HealthResponse, SystemInfoResponse

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
