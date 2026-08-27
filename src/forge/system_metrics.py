from datetime import UTC, datetime
from pathlib import Path

import psutil

from forge.logging_config import get_logger
from forge.schemas import CurrentMetricsResponse

logger = get_logger(__name__)


class MetricsCollectionError(RuntimeError):
    """Raised when Forge cannot collect system metrics."""


def collect_current_metrics() -> CurrentMetricsResponse:
    try:
        disk_root = Path.cwd().anchor

        return CurrentMetricsResponse(
            cpu_percent=psutil.cpu_percent(interval=0.1),
            memory_percent=psutil.virtual_memory().percent,
            disk_percent=psutil.disk_usage(disk_root).percent,
            collected_at=datetime.now(UTC),
        )
    except (OSError, psutil.Error) as error:
        logger.exception("Failed to collect current system metrics")
        raise MetricsCollectionError(
            "Current system metrics could not be collected"
        ) from error
