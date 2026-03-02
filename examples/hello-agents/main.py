"""
Hello Agents API - Simple REST API with health check endpoints.

This API provides three endpoints:
- GET / - Root endpoint returning status
- GET /health - Health check endpoint
- GET /version - API version information
"""
from fastapi import FastAPI
from pydantic import BaseModel
import os

# FastAPI application instance
app = FastAPI(
    title="Hello Agents API",
    version="1.0.0",
    description="Simple REST API with health check endpoints"
)

# Response models
class StatusResponse(BaseModel):
    """Response model for status endpoints."""
    status: str


class VersionResponse(BaseModel):
    """Response model for version endpoint."""
    version: str


# Configuration
API_VERSION = os.getenv("API_VERSION", "1.0.0")


@app.get("/", response_model=StatusResponse)
def root() -> StatusResponse:
    """
    Root endpoint to verify API is running.
    
    Returns:
        StatusResponse: JSON response with status "ok"
    """
    return StatusResponse(status="ok")


@app.get("/health", response_model=StatusResponse)
def health() -> StatusResponse:
    """
    Health check endpoint for monitoring.
    
    Returns:
        StatusResponse: JSON response with status "healthy"
    """
    return StatusResponse(status="healthy")


@app.get("/version", response_model=VersionResponse)
def version() -> VersionResponse:
    """
    API version information endpoint.
    
    Returns:
        VersionResponse: JSON response with API version
    """
    return VersionResponse(version=API_VERSION)
