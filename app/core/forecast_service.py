"""Business logic with LLM fallback and timing."""
import time
from app.services.weather import weather_service
from app.services.llm import llm_service
from app.prompts import get_fallback_forecast


class ForecastService:
    """Orchestrates forecast generation with fallback and timing."""
    
    async def generate_forecast(self, persona: str, style: str) -> str:
        """
        Generate forecast with LLM, fallback to hardcoded on error.
        
        Returns forecast text and prints timing breakdown.
        """
        
        total_start = time.time()
        weather_time = 0
        llm_time = 0
        
        try:
            # Fetch weather
            print("  Fetching weather from Open-Meteo...")
            weather_start = time.time()
            weather_data = await weather_service.get_forecast(days=2)
            weather_summary = weather_service.format_weather_summary(weather_data)
            weather_time = time.time() - weather_start
            print(f"   └─ Weather API fetch: {weather_time:.2f}s")
            
            # Generate with LLM
            print(f" Generating forecast with LLM (persona='{persona}', style='{style}')...")
            llm_start = time.time()
            forecast = await llm_service.generate_forecast(
                weather_data=weather_summary,
                persona=persona,
                style=style
            )
            llm_time = time.time() - llm_start
            print(f"   └─ LLM generation: {llm_time:.2f}s")
            
            print("✅ LLM generation successful")
            
            # Print timing breakdown
            total_time = time.time() - total_start
            print(f"\n  Timing Breakdown:")
            print(f"├─ Weather API fetch         {weather_time:.2f}s")
            print(f"├─ LLM generation            {llm_time:.2f}s")
            print(f"└─ Total response time       {total_time:.2f}s\n")
            
            return forecast
        
        except Exception as e:
            # Fallback to hardcoded
            print(f"  LLM/API failed: {str(e)}")
            print(f" Using hardcoded fallback (persona='{persona}', style='{style}')")
            
            fallback = get_fallback_forecast(persona, style)
            
            total_time = time.time() - total_start
            print(f"\n  Fallback response time: {total_time:.2f}s\n")
            
            return fallback


# Global service instance
forecast_service = ForecastService()