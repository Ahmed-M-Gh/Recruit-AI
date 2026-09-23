from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path
from functools import lru_cache
from enum import Enum

BASE_DIR = Path(__file__).resolve().parent.parent

    
class Settings(BaseSettings):
    # App Information
    APP_NAME:str
    APP_VERSION:str
    
    # LLM Settings
    LLM_MODEL:str = "openai/gpt-oss-120b"
    LLM_API_KEY:str
    LLM_BASE_URL:str = "https://api.groq.com/openai/v1" 
    LLM_TIMEOUT:float = 30.0
    LLM_MAX_RETRIES:int = 2
    LLM_TEMPERATURE:float = 0.3
    LLM_MAX_TOKENS:int = 2048
    
    # env file
    model_config = SettingsConfigDict(
        env_file=BASE_DIR/".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )
        
@lru_cache        
def get_settings() -> Settings:
    return Settings()

# Response messages
class ResponseSignal(Enum):
    
    RATE_LIMIT = "Groq API Limit Exceeded."
    API_TIME_OUT = "Groq API Timeout."
