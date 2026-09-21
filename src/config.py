from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

class Settings(BaseSettings):
    # App Information
    APP_NAME:str
    APP_VERSION:str
    
    
    # env file
    model_config = SettingsConfigDict(
        env_file=BASE_DIR/".env",
        env_file_encoding="utf-8"
    )
        
        
def get_settings():
    return Settings()