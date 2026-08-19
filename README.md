# Forge

Forge is a Python backend project for infrastructure monitoring and automation.

The project is being developed incrementally as a portfolio-quality demonstration of backend software engineering. Its initial focus is a reliable FastAPI foundation that can later support system metrics, historical monitoring, Linux deployment, home-lab devices, automation, and carefully scoped AI-assisted analysis.

## Current status

Forge is in Phase 1 of development.

The current application provides:

- A FastAPI application entry point.
- A health-check endpoint at `GET /health`.
- A system-information endpoint at `GET /system`.
- Typed response schemas using Pydantic.
- Automated API tests for both endpoints.
- Python 3.13 project configuration.
- An isolated local development environment.

## Technology

- Python 3.13
- FastAPI
- Uvicorn
- Pydantic
- Git
- pytest

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

`FORGE_ENVIRONMENT` accepts `development`, `testing`, or `production`.

The local `.env` file is ignored by Git and must not contain values intended for version control.

## Running tests

Install Forge with its development dependencies:

```powershell
python -m pip install --editable ".[dev]"
```

Run the automated test suite:

```powershell
python -m pytest
```

The current tests verify the health response and the live system information returned by the machine running Forge.

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

## Project structure

```text
Forge/
|-- src/
|   `-- forge/
|       |-- __init__.py
|       |-- main.py
|       `-- schemas.py
|-- tests/
|   |-- test_health.py
|   `-- test_system.py
|-- .gitignore
|-- pyproject.toml
`-- README.md
```