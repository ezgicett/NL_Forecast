"""Forecast-related endpoints."""
from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import PlainTextResponse
from app.constants import VALID_PERSONAS, VALID_STYLES
from app.core.forecast_service import forecast_service
from app.config import settings

router = APIRouter(tags=["Forecast"])


@router.get(
    "/nl-forecast",
    response_class=PlainTextResponse,
    summary="Get Berlin weather forecast",
    description="Original requirement endpoint with hardcoded persona/style from env."
)
async def get_nl_forecast():
    """
    Get 2-day Berlin weather forecast (hardcoded settings).
    
    Uses DEFAULT_PERSONA and DEFAULT_STYLE from .env file.
    Returns text/plain response with natural language forecast.
    """
    print(f" Hardcoded endpoint called")
    print(f"   ├─ Persona: {settings.default_persona}")
    print(f"   └─ Style: {settings.default_style}")
    
    forecast_text = await forecast_service.generate_forecast(
        persona=settings.default_persona,
        style=settings.default_style
    )
    
    return PlainTextResponse(forecast_text)


@router.get(
    "/forecast",
    response_class=PlainTextResponse,
    summary="Get customizable Berlin forecast",
    description="Flexible endpoint for testing different personas and styles."
)
async def get_custom_forecast(
    persona: str = Query(
        default="runner",
        description="Target persona: runner, tourist, local, photographer"
    ),
    style: str = Query(
        default="newsy",
        description="Writing style: newsy, emoji, casual, technical"
    )
):
    """
    Get 2-day Berlin weather forecast with custom persona and style.
    
    Bonus endpoint for testing. Main requirement is /nl-forecast.
    """
    # Validation
    if persona not in VALID_PERSONAS:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid persona '{persona}'. Must be one of: {', '.join(VALID_PERSONAS)}"
        )
    
    if style not in VALID_STYLES:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid style '{style}'. Must be one of: {', '.join(VALID_STYLES)}"
        )
    
    print(f" Custom endpoint called")
    print(f"   ├─ Persona: {persona}")
    print(f"   └─ Style: {style}")
    
    forecast_text = await forecast_service.generate_forecast(persona, style)
    
    return PlainTextResponse(forecast_text)