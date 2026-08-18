import platform
import socket
from datetime import UTC, datetime

from fastapi.testclient import TestClient

from forge.main import app

client = TestClient(app)


def test_system_info_returns_current_host_details() -> None:
    before_request = datetime.now(UTC)

    response = client.get("/system")

    after_request = datetime.now(UTC)
    data = response.json()
    collected_at = datetime.fromisoformat(data["collected_at"])

    assert response.status_code == 200
    assert data["hostname"] == socket.gethostname()
    assert data["operating_system"] == platform.system()
    assert data["python_version"] == platform.python_version()
    assert before_request <= collected_at <= after_request
