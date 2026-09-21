"""Dépendances FastAPI pour la gestion de l'authentification et l'extraction de l'utilisateur."""

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from pydantic import BaseModel

from core.config import settings

# Indique à FastAPI que la route pour obtenir le token est /auth/login
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


# Structure interne pour valider le contenu décodé du token
class TokenData(BaseModel):
    email: str | None = None


async def get_current_user(token: str = Depends(oauth2_scheme)) -> str:
    """Décode le token JWT et extrait l'email de l'utilisateur connecté. Lève une exception HTTP 401 si le token est invalide ou expiré."""

    credentials_exception = HTTPException(
        status_code=401,
        detail="Jeton d'authentification invalide ou expiré",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        # Décodage du jeton avec la clé secrète
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except JWTError:
        raise credentials_exception

    # Retourne l'email extrait du token en attendant la BDD
    return token_data.email