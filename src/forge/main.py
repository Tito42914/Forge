from fastapi import FastAPI

app = FastAPI(
    title="Forge",
    version="0.1.0",
)

@app.get("/health")
def read_health() -> dict[str, str]:
    return {"status": "healthy"}