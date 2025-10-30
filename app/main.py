"""Main FastAPI application."""
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from app.api import ui, forecast, health
from app.middleware.timing import TimingMiddleware
from app import __version__

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup and shutdown events."""
    print(" Weather API starting up...")
    print(" Services initialized")
    yield
    print("👋 Weather API shutting down...")


app = FastAPI(
    title="Berlin Weather Forecast API",
    description="A tiny web API for 2-day weather forecasts with persona-based natural language generation",
    version=__version__,
    lifespan=lifespan
)

# Add timing middleware
app.add_middleware(TimingMiddleware)

# Register routers
app.include_router(ui.router)
app.include_router(forecast.router)
app.include_router(health.router)

# Custom 404 handler
@app.exception_handler(404)
async def not_found_handler(request: Request, exc):
    """User-friendly 404 error handler."""
    return JSONResponse(
        status_code=404,
        content={
            "message": "Endpoint not found. Available endpoints: GET /nl-forecast, GET /forecast, GET /health"
        }
    )