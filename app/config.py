"""Configuration settings using Pydantic."""
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # OpenAI
    openai_api_key: str
    llm_model: str = "gpt-4o-mini"
    llm_max_tokens: int = 150
    llm_temperature: float = 0.3
    
    # Berlin coordinates
    berlin_lat: float = 52.52
    berlin_lon: float = 13.41
    
    # Default forecast settings
    default_persona: str = "runner"
    default_style: str = "newsy"
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False
    )


# Global settings instance
settings = Settings()