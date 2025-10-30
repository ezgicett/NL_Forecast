"""Pydantic models for request and response validation."""
from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    """Health check response."""
    status: str = "healthy"
    message: str = "Weather API is running"