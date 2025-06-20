from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    DB_HOST: str = "localhost"
    DB_PORT: int = 3306
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str

    # Application settings
    DEBUG: bool = True
    LOG_LEVEL: str = "INFO"
    APP_NAME: str = "Smart Notes API"

    # AI Service Settings
    AI_API_KEY: str

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()