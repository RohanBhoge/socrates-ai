from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    # API Configuration
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    
    # Gemini API
    GEMINI_API_KEY: str = "AIzaSyDiYiVW2CLVwLt8OClkjkxJJc5WOAWo6vw" # Optional to allow startup without key
    GEMINI_MODEL: str = "gemini-2.5-flash"
    
    # CORS
    ALLOWED_ORIGINS: List[str] = ["http://localhost:3000"]
    
    # File Upload
    MAX_FILE_SIZE: int = 10 * 1024 * 1024  # 10MB
    UPLOAD_DIR: str = "./uploads"
    
    # Memory Store
    MEMORY_BACKEND: str = "inmemory"  # Options: inmemory, redis
    REDIS_URL: str = "redis://localhost:6379"
    
    # Session
    SESSION_TTL_HOURS: int = 24
    
    class Config:
        env_file = ".env"

settings = Settings()
