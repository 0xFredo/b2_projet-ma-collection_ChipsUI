"""Dépendances FastAPI pour la gestion de l'authentification et l'extraction de l'utilisateur."""

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from pydantic import BaseModel
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import settings
from db.database import AsyncSessionLocal
from dependencies.db import get_session
from models.user import User

# Indique à FastAPI que la route pour obtenir le token est /auth/login
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


class TokenData(BaseModel):
    email: str | None = None


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    session: AsyncSession = Depends(get_session)
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Jeton d'authentification invalide ou expiré",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    # On cherche l'utilisateur par son ID (en le convertissant en entier)
    try:
        statement = select(User).where(User.id == int(user_id))
        result = await session.execute(statement)
        user = result.scalar_one_or_none()
    except ValueError:
        raise credentials_exception

    if user is None:
        raise credentials_exception

    return user