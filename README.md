# Forge

Forge is a Python backend project for infrastructure monitoring and automation.

The project is being developed incrementally as a portfolio-quality demonstration of backend software engineering. Its initial focus is a reliable FastAPI foundation that can later support system metrics, historical monitoring, Linux deployment, home-lab devices, automation, and carefully scoped AI-assisted analysis.

## Current status

Forge has completed Phase 1: a portfolio-ready Python backend foundation.
The `v0.1.0` milestone provides a tested, configurable and observable API for
current host information and resource monitoring.

Phase 2 will introduce relational data modelling and historical metric
persistence without expanding the completed Phase 1 scope.

The current application provides:

- A FastAPI application entry point.
- A health-check endpoint at `GET /health`.
- A system-information endpoint at `GET /system`.
- A current resource-metrics endpoint at `GET /metrics/current`.
- Intentional `503 Service Unavailable` handling for metrics collection failures.
- Configurable application logging with startup and shutdown messages.
- Typed response schemas using Pydantic.
- Automated API tests for the application endpoints and configuration.
- Python 3.13 project configuration.
- An isolated local development environment.

## Technology

- Python 3.13
- FastAPI
- Uvicorn
- Pydantic
- Pydantic Settings
- psutil
- Python standard-library logging
- pytest
- Ruff
- Git and GitHub
- GitHub Actions

## Configuration

Forge provides default development settings and can be configured with environment variables or a local `.env` file.

To create a local configuration file in PowerShell:

```powershell
Copy-Item .env.example .env
```

Supported variables:

- `FORGE_APP_NAME`
- `FORGE_APP_VERSION`
- `FORGE_ENVIRONMENT`
- `FORGE_LOG_LEVEL`

`FORGE_ENVIRONMENT` accepts `development`, `testing`, or `production`.
`FORGE_LOG_LEVEL` accepts `DEBUG`, `INFO`, `WARNING`, `ERROR`, or `CRITICAL`.

The local `.env` file is ignored by Git and must not contain values intended for version control.

## Running Forge

Install Forge with its development dependencies:

```powershell
python -m pip install --editable ".[dev]"
```

Start the development server:

```powershell
python -m uvicorn forge.main:app --reload
```

The API is then available at `http://127.0.0.1:8000`. Interactive API
documentation is available at `http://127.0.0.1:8000/docs`.

## Running tests

Run the automated test suite:

```powershell
python -m pytest
```

The current tests cover application configuration, logging, API responses,
resource-metric validation, service behavior, and metrics collection failures.

## API endpoints

### `GET /health`

Reports whether the Forge application is running.

Example response:

```json
{
  "status": "healthy"
}
```

### `GET /system`

Returns basic information about the machine running Forge:

- Hostname
- Operating system
- Python version
- UTC collection timestamp

Example response:

```json
{
  "hostname": "example-host",
  "operating_system": "Windows",
  "python_version": "3.13.5",
  "collected_at": "2026-08-17T14:25:14.714464Z"
}
```

### `GET /metrics/current`

Returns a current snapshot of the host machine's resource usage:

- CPU usage
- Memory usage
- Disk usage
- UTC collection timestamp

Example response:

```json
{
  "cpu_percent": 4.2,
  "memory_percent": 69.9,
  "disk_percent": 95.7,
  "collected_at": "2026-08-20T16:21:41.620674Z"
}
```

Metrics collection is separated from the HTTP route. If Forge cannot retrieve
the current resource data, the failure is logged and the endpoint returns a
documented `503 Service Unavailable` response.

## Project structure

```text
Forge/
|-- .github/
|   `-- workflows/
|       `-- ci.yml
|-- src/
|   `-- forge/
|       |-- __init__.py
|       |-- config.py
|       |-- logging_config.py
|       |-- main.py
|       |-- schemas.py
|       `-- system_metrics.py
|-- tests/
|   |-- test_config.py
|   |-- test_health.py
|   |-- test_logging_config.py
|   |-- test_metrics.py
|   |-- test_system_metrics.py
|   `-- test_system.py
|-- .env.example
|-- .gitignore
|-- pyproject.toml
`-- README.md
```
