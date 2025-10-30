"""LLM prompt templates + hardcoded fallbacks."""
from app.constants import PERSONA_DESCRIPTIONS, STYLE_DESCRIPTIONS

# Hardcoded fallback forecasts
HARDCODED_FORECASTS = {
    ("runner", "newsy"): """Runner's Berlin forecast: Today brings comfortable conditions with temperatures around 16-20°C and light winds under 15 km/h—ideal for outdoor training. Tomorrow expect similar conditions with a slight chance of afternoon showers, so plan your morning run accordingly.""",
    
    ("runner", "emoji"): """🏃‍♂️ Today: 18°C, light winds 🌬️ Perfect for running! 
🌧️ Tomorrow: 17°C, 30% rain chance ☔ Morning run recommended!""",
    
    ("runner", "casual"): """Hey runner! Today's looking pretty sweet for a run - around 18°C with nice light winds. Tomorrow's gonna be similar but there's a chance of some rain in the afternoon, so maybe hit the pavement in the morning if you can!""",
    
    ("runner", "technical"): """Temperature range: 16-20°C. Wind: NW 8-14 km/h. Precipitation probability: <10% today, 30% tomorrow afternoon. Conditions optimal for endurance training both days, with morning sessions preferred tomorrow.""",
    
    ("tourist", "newsy"): """Berlin's weather welcomes tourists with pleasant conditions today—temperatures reaching 18-20°C under partly cloudy skies. Perfect for exploring outdoor attractions and walking tours. Tomorrow brings similar comfort levels with a slight chance of afternoon showers, so keep an umbrella handy for evening plans.""",
    
    ("tourist", "emoji"): """ Today: 19°C, partly cloudy ☁️ Great for sightseeing!
☂️ Tomorrow: 18°C, possible rain 🌧️ Bring umbrella for afternoon!""",
    
    ("tourist", "casual"): """Hey there! Berlin's treating you well today - nice 19°C weather, perfect for hitting up those tourist spots. Tomorrow's pretty much the same but might get a bit rainy in the afternoon, so maybe pack that umbrella just in case!""",
    
    ("tourist", "technical"): """Temperature: 17-20°C. Cloud cover: 40-60%. Precipitation: <5% today, 25% tomorrow PM. Visibility: Excellent. Optimal conditions for outdoor activities and photography. UV index: Moderate.""",
    
    ("local", "newsy"): """Berlin locals can expect typical autumn weather today with temperatures around 16-19°C—comfortable for the commute with no significant weather disruptions. Tomorrow maintains these conditions with a possibility of brief afternoon showers, though nothing that should affect daily routines.""",
    
    ("local", "emoji"): """🏠 Today: 18°C, normal day ☀️ Regular commute conditions
🌧️ Tomorrow: 17°C, brief showers possible 💧 Nothing major""",
    
    ("local", "casual"): """Pretty standard Berlin weather today - around 18°C, nothing crazy. Should be fine for your commute and whatever you've got planned. Tomorrow's the same deal, maybe some light rain later but nothing to stress about.""",
    
    ("local", "technical"): """Temperature: 16-19°C. Wind: 10-15 km/h. Conditions stable for commute. Tomorrow: Similar parameters with 20% precipitation probability 1400-1800 hours. No weather advisories.""",
    
    ("photographer", "newsy"): """Photographers will find Berlin offering mixed lighting today with partial cloud cover creating interesting contrast opportunities—golden hour should be particularly striking. Tomorrow presents similar conditions with slightly increased cloud cover, potentially dramatic for landscape and urban photography.""",
    
    ("photographer", "emoji"): """📷 Today: Partly cloudy ☁️✨ Great golden hour conditions!
🌅 Tomorrow: More clouds 🌥️ Dramatic lighting potential!""",
    
    ("photographer", "casual"): """Pretty nice shooting weather today! You've got those partial clouds that'll give you some interesting light to work with. Golden hour should be awesome. Tomorrow's got a bit more cloud cover, could make for some really moody shots if that's your thing.""",
    
    ("photographer", "technical"): """Cloud cover: 40-50% today, 60-70% tomorrow. Golden hour: 1730-1800 CET. Visibility: 15+ km. Lighting conditions favorable for contrast work. Sunrise: 0742, Sunset: 1723. Increased diffusion tomorrow suitable for portraiture."""
}


def get_fallback_forecast(persona: str, style: str) -> str:
    """Get hardcoded fallback forecast."""
    key = (persona, style)
    return HARDCODED_FORECASTS.get(
        key,
        f"Weather forecast unavailable for {persona} in {style} style."
    )


def build_system_prompt() -> str:
    """Build generic system prompt."""
    return """You are a Berlin weather forecasting assistant. Provide clear, actionable 2-day forecasts.

OUTPUT RULES:
- 2-5 complete sentences
- Round temps to whole numbers
- Use descriptive terms (mild, chilly, warm) alongside numbers and highlight extremes(very hot/cold, heavy rain, high winds)
- Emphasize conditions relevant to the audience"""

def build_user_prompt(persona: str, style: str, weather_data: str) -> str:
    """Build concise user prompt."""
    persona_desc = PERSONA_DESCRIPTIONS[persona]
    style_desc = STYLE_DESCRIPTIONS[style]
    
    return f"""Weather (Berlin, 2 days):
{weather_data}

Audience: {persona} - {persona_desc}
Style: {style} - {style_desc}
"""