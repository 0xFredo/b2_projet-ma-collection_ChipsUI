"""Configuration globale de l'application et chargement des variables d'environnement."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Schéma de configuration chargé depuis le fichier .env."""

    PROJECT_NAME: str = "API Collection"

    # Base de données SQLite asynchrone (SQLModel + aiosqlite)
    DATABASE_URL: str = "sqlite+aiosqlite:///./app.db"

    # Sécurité & JWT (HS256)
    SECRET_KEY: str = "CHANGE_ME_IN_PRODUCTION_SECRET_KEY_123456789"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # Durée de validité du jeton JWT (24 heures)

    # Indique à Pydantic de lire le fichier .env et d'ignorer les variables en trop
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


# Instance unique (Singleton) réutilisée dans toute l'application
settings = Settings()