import pytest

from forge.config import Settings


def test_settings_use_defaults(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("FORGE_APP_NAME", raising=False)
    monkeypatch.delenv("FORGE_APP_VERSION", raising=False)
    monkeypatch.delenv("FORGE_ENVIRONMENT", raising=False)

    settings = Settings(_env_file=None)

    assert settings.app_name == "Forge"
    assert settings.app_version == "0.1.0"
    assert settings.environment == "development"


def test_settings_read_environment_variables(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("FORGE_APP_NAME", "Forge Test")
    monkeypatch.setenv("FORGE_APP_VERSION", "9.9.9")
    monkeypatch.setenv("FORGE_ENVIRONMENT", "testing")

    settings = Settings(_env_file=None)

    assert settings.app_name == "Forge Test"
    assert settings.app_version == "9.9.9"
    assert settings.environment == "testing"
