from unittest.mock import Mock

import pytest

from forge.system_metrics import MetricsCollectionError, collect_current_metrics


def test_collect_current_metrics_translates_os_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def raise_os_error(*, interval: float) -> float:
        raise OSError(f"Simulated failure at interval {interval}")

    log_exception = Mock()

    monkeypatch.setattr(
        "forge.system_metrics.psutil.cpu_percent",
        raise_os_error,
    )
    monkeypatch.setattr(
        "forge.system_metrics.logger.exception",
        log_exception,
    )

    with pytest.raises(MetricsCollectionError) as error_info:
        collect_current_metrics()

    assert str(error_info.value) == ("Current system metrics could not be collected")
    assert isinstance(error_info.value.__cause__, OSError)
    log_exception.assert_called_once_with("Failed to collect current system metrics")
