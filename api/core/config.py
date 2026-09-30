"""Configuration globale de l'application et chargement des variables d'environnement."""
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Schéma de configuration chargé depuis le fichier .env."""

    PROJECT_NAME: str = "API Collection"

    # Base de données postgre
    DATABASE_URL: str

    # Sécurité & JWT (HS256)
    SECRET_KEY: str = Field(..., min_length=32) # 32 caracteres minimum
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # Durée de validité du jeton JWT (24 heures)

    # Indique à Pydantic de lire le fichier .env et d'ignorer les variables en trop
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


# Instance unique (Singleton) réutilisée dans toute l'application
settings = Settings()