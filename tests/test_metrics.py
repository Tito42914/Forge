from datetime import UTC, datetime

from fastapi.testclient import TestClient

from forge.main import app

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
