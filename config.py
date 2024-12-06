from decouple import config
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    OPENAI_API_KEY: str
    
    
def get_settings() -> Settings:
    return Settings(OPENAI_API_KEY=config('OPENAI_API', default=''))

settings = get_settings()