# Lecture des variables du .env
"""Configuration globale de l'application FastAPI."""

import os
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str = "API Collection"
    
    # Base de données
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./app.db")
    
    # Sécurité & JWT (HS256)
    SECRET_KEY: str = os.getenv("SECRET_KEY", "CHANGE_ME_IN_PRODUCTION_SECRET_KEY_123456789")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # Token valide 24h

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()