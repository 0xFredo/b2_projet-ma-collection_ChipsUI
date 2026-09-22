"""Schémas Pydantic pour la validation des données Utilisateur."""

from pydantic import BaseModel, EmailStr, ConfigDict


# Données communes à tous les schémas utilisateur
class UserBase(BaseModel):
    email: EmailStr


# Données reçues à l'inscription (POST /auth/register)
class UserCreate(UserBase):
    password: str


# Données renvoyées par l'API (masque le mot de passe)
class UserRead(UserBase):
    id: int
    is_admin: bool = False
    model_config = ConfigDict(from_attributes=True)


# Schéma pour la réponse du Token JWT (POST /auth/login)
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"