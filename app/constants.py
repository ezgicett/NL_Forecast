"""Single source of truth for personas and styles."""

VALID_PERSONAS = ["runner", "tourist", "local", "photographer"]
VALID_STYLES = ["newsy", "emoji", "casual", "technical"]

PERSONA_DESCRIPTIONS = {
    "runner": "Focus on running conditions: temperature, wind, precipitation. Mention if good for outdoor running.",
    "tourist": "Focus on sightseeing comfort, what to wear, outdoor activities.",
    "local": "Focus on commute conditions, daily planning, weather extremes.",
    "photographer": "Focus on lighting, golden hour, cloud cover, photography conditions."
}

STYLE_DESCRIPTIONS = {
    "newsy": "Journalistic paragraph.",
    "emoji": "Concise with relevant emojis.",
    "casual": "Friendly conversational tone.",
    "technical": "Precise metrics and measurements."
}