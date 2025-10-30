"""Open-Meteo API client for fetching weather data."""
import httpx
from typing import Dict, Any
from app.config import settings


class WeatherService:
    """Service for fetching weather data from Open-Meteo API."""
    
    BASE_URL = "https://api.open-meteo.com/v1/forecast"
    
    async def get_forecast(self, days: int = 2) -> Dict[str, Any]:
        """Fetch weather forecast for Berlin."""
        params = {
            "latitude": settings.berlin_lat,
            "longitude": settings.berlin_lon,
            "forecast_days": days,
            "daily": [
                "temperature_2m_max",
                "temperature_2m_min",
                "precipitation_sum",
                "precipitation_probability_max",
                "windspeed_10m_max",
                "weathercode"
            ],
            "timezone": "Europe/Berlin"
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.get(
                self.BASE_URL,
                params=params,
                timeout=10.0
            )
            response.raise_for_status()
            return response.json()
    
    def format_weather_summary(self, data: Dict[str, Any]) -> str:
        """Format raw weather data into readable summary for LLM."""
        daily = data.get("daily", {})
        
        summary_lines = []
        
        for i, date in enumerate(daily.get("time", [])):
            day_label = "Today" if i == 0 else "Tomorrow"
            
            temp_max = daily["temperature_2m_max"][i]
            temp_min = daily["temperature_2m_min"][i]
            precip = daily["precipitation_sum"][i]
            precip_prob = daily["precipitation_probability_max"][i]
            wind = daily["windspeed_10m_max"][i]
            
            summary = (
                f"{day_label} ({date}): "
                f"Temp {temp_min}°C - {temp_max}°C, "
                f"Precip {precip}mm ({precip_prob}% prob), "
                f"Wind up to {wind} km/h"
            )
            
            summary_lines.append(summary)
        
        return "\n".join(summary_lines)


# Global service instance
weather_service = WeatherService()