# Forge

Forge is a Python backend project for infrastructure monitoring and automation.

The project is being developed incrementally as a portfolio-quality demonstration of backend software engineering. Its initial focus is a reliable FastAPI foundation that can later support system metrics, historical monitoring, Linux deployment, home-lab devices, automation, and carefully scoped AI-assisted analysis.

## Current status

Forge is in Phase 1 of development.

The current application provides:

- A FastAPI application entry point.
- A health-check endpoint at `GET /health`.
- Python 3.13 project configuration.
- An isolated local development environment.
- An automated API test for the health endpoint.

## Technology

- Python 3.13
- FastAPI
- Uvicorn
- Pydantic
- Git
- pytest

## Running tests

Install Forge with its development dependencies:

```powershell
python -m pip install --editable ".[dev]"
```

Run the automated test suite:

```powershell
python -m pytest
```

The current test verifies that `GET /health` returns HTTP `200 OK` and the expected JSON response.


## Project structure

```text
Forge/
├── src/
│   └── forge/
│       ├── __init__.py
│       └── main.py
├── .gitignore
├── pyproject.toml
└── README.md