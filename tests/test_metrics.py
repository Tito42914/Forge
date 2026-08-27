from datetime import UTC, datetime

import pytest
from fastapi.testclient import TestClient
from pydantic import ValidationError

from forge.main import app
from forge.schemas import CurrentMetricsResponse
from forge.system_metrics import MetricsCollectionError

client = TestClient(app)


def test_current_metrics_returns_resource_usage() -> None:
    before_request = datetime.now(UTC)

    response = client.get("/metrics/current")

    after_request = datetime.now(UTC)
    data = response.json()
    collected_at = datetime.fromisoformat(data["collected_at"])

    assert response.status_code == 200
    assert 0 <= data["cpu_percent"] <= 100
    assert 0 <= data["memory_percent"] <= 100
    assert 0 <= data["disk_percent"] <= 100
    assert before_request <= collected_at <= after_request


@pytest.mark.parametrize(
    ("field_name", "invalid_value"),
    [
        ("cpu_percent", -0.1),
        ("cpu_percent", 100.1),
        ("memory_percent", -0.1),
        ("memory_percent", 100.1),
        ("disk_percent", -0.1),
        ("disk_percent", 100.1),
    ],
)
def test_current_metrics_rejects_invalid_percentages(
    field_name: str,
    invalid_value: float,
) -> None:
    metrics = {
        "cpu_percent": 25.0,
        "memory_percent": 50.0,
        "disk_percent": 75.0,
        "collected_at": datetime.now(UTC),
    }
    metrics[field_name] = invalid_value

    with pytest.raises(ValidationError):
        CurrentMetricsResponse(**metrics)


def test_current_metrics_returns_503_when_collection_fails(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def raise_metrics_collection_error() -> CurrentMetricsResponse:
        raise MetricsCollectionError("Simulated metrics failure")

    monkeypatch.setattr(
        "forge.main.collect_current_metrics",
        raise_metrics_collection_error,
    )

    response = client.get("/metrics/current")

    assert response.status_code == 503
    assert response.json() == {
        "detail": "Current system metrics are temporarily unavailable"
    }
