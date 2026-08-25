import pytest

from forge.logging_config import configure_logging, get_logger


def test_configure_logging_filters_and_formats_messages(
    capsys: pytest.CaptureFixture[str],
) -> None:
    configure_logging("INFO")
    logger = get_logger("forge.test")

    logger.debug("Hidden debug message")
    logger.info("Visible info message")

    captured = capsys.readouterr()

    assert "Hidden debug message" not in captured.out
    assert "Visible info message" in captured.out
    assert "INFO | forge.test" in captured.out
