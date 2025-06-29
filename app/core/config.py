from pydantic_settings import BaseSettings

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
    GITHUB_TOKEN: str

    # Authentication Settings
    SECRET_KEY: str
    ALGORITHM: str = "HS256"

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()