from openai import AsyncOpenAI
from src.config import get_settings

settings = get_settings()

llm_client = AsyncOpenAI(
    api_key=settings.LLM_API_KEY,
    base_url=settings.LLM_BASE_URL,
    timeout=settings.LLM_TIMEOUT,
    max_retries=settings.LLM_MAX_RETRIES
)

def get_llm_client() -> AsyncOpenAI:
    """Returns the singleton AsyncOpenAI instance."""
    return llm_client