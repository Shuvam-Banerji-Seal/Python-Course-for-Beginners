"""
FastAPI example application using uv for dependency management.
"""

from fastapi import FastAPI
from pydantic import BaseModel
import httpx

app = FastAPI(title="UV Project Example", version="0.1.0")

class HealthResponse(BaseModel):
    status: str
    message: str

class ExternalAPIResponse(BaseModel):
    data: dict
    source: str

@app.get("/")
async def root():
    """Root endpoint."""
    return {"message": "Hello from UV project!"}

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    return HealthResponse(
        status="healthy",
        message="Application is running correctly"
    )

@app.get("/external", response_model=ExternalAPIResponse)
async def fetch_external_data():
    """Fetch data from external API."""
    async with httpx.AsyncClient() as client:
        response = await client.get("https://httpbin.org/json")
        return ExternalAPIResponse(
            data=response.json(),
            source="httpbin.org"
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)