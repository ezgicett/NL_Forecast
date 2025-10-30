"""OpenAI LLM client for generating natural language forecasts."""
from openai import AsyncOpenAI
from app.config import settings
from app.prompts import build_system_prompt, build_user_prompt


class LLMService:
    """Service for generating natural language responses using OpenAI."""
    
    def __init__(self):
        self.client = AsyncOpenAI(api_key=settings.openai_api_key)
    
    async def generate_forecast(
        self,
        weather_data: str,
        persona: str = None, # fetch from config
        style: str = None    #fetch from config
    ) -> str:
        """Generate natural language forecast using LLM."""
        # Get default values from config
        persona = persona or settings.default_persona
        style = style or settings.default_style
        
        system_prompt = build_system_prompt()
        user_prompt = build_user_prompt(persona, style, weather_data)
        
        system_words = len(system_prompt.split())
        user_words = len(user_prompt.split())
        estimated_tokens = int((system_words + user_words) * 1.3)
        
        print(f" Estimated input tokens: ~{estimated_tokens}")
        print(f"   ├─ System prompt: ~{system_words} words")
        print(f"   └─ User prompt: ~{user_words} words")
        
        try:
            response = await self.client.chat.completions.create(
                model=settings.llm_model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                max_tokens=settings.llm_max_tokens,
                temperature=settings.llm_temperature
            )
            
            # Actual token usage (real values from OpenAI)
            usage = response.usage
            print(f" Actual token usage:")
            print(f"   ├─ Input tokens: {usage.prompt_tokens}")
            print(f"   ├─ Output tokens: {usage.completion_tokens}")
            print(f"   └─ Total tokens: {usage.total_tokens}")
            
            # Actual and estimated token count comparision
            accuracy = (estimated_tokens / usage.prompt_tokens) * 100 if usage.prompt_tokens > 0 else 0
            print(f"   └─ Estimation accuracy: {accuracy:.0f}%")
            
            return response.choices[0].message.content.strip()
        
        except Exception as e:
            raise Exception(f"LLM generation failed: {str(e)}")


# Global service instance
llm_service = LLMService()