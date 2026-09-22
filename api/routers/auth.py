from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from core.config import settings
from core.security import create_access_token, get_password_hash, verify_password
from dependencies.auth import get_current_user
from dependencies.db import get_session
from models.user import User
from schemas.user import UserCreate, UserRead, Token

# Initialisation du routeur dédié à l'authentification
router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post(
    "/register", 
    response_model=UserRead, 
    status_code=status.HTTP_201_CREATED,
    summary="Inscription d'un nouvel utilisateur",
    response_description="L'utilisateur créé sans ses données sensibles."
)
async def register(
    user_data: UserCreate,
    session: Annotated[AsyncSession, Depends(get_session)]
):
    """
    Inscrit un nouvel utilisateur dans le système.

    - **user_data**: Données de création de l'utilisateur (email, mot de passe, etc.).
    - **session**: Session active de la base de données SQLite.

    **Déroulement :**
    1. Vérifie si l'adresse e-mail existe déjà en base de données.
    2. Hache le mot de passe via l'algorithme sécurisé (bcrypt).
    3. Enregistre le nouvel utilisateur en base de données.
    4. Retourne le profil créé filtré par le schéma `UserPublic` (sans le hash du mot de passe).

    **Erreurs possibles :**
    - `400 BAD REQUEST` : Si l'adresse e-mail est déjà associée à un compte.
    """
    # 1. Vérification de l'existence préalable de l'utilisateur
    result = await session.execute(select(User).where(User.email == user_data.email))
    existing_user = result.scalars().first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Un compte existe déjà avec cet email."
        )

    # 2. Hachage sécurisé du mot de passe avant persistance
    hashed_password = get_password_hash(user_data.password)
    
    # 3. Instanciation du modèle ORM pour la BDD
    db_user = User(
        email=user_data.email,
        hashed_password=hashed_password,
        role=user_data.role if hasattr(user_data, 'role') else "user"
    )
    
    # 4. Sauvegarde en base de données
    session.add(db_user)
    await session.commit()
    await session.refresh(db_user)

    return db_user


@router.post(
    "/login", 
    response_model=Token,
    summary="Connexion et génération du token JWT",
    response_description="Le jeton d'accès JWT et son type (Bearer)."
)
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: Annotated[AsyncSession, Depends(get_session)]
):
    """
    Authentifie l'utilisateur via ses identifiants OAuth2.

    - **form_data**: Formulaire standardisé OAuth2 contenant `username` (email) et `password`.
    - **session**: Session active de la base de données.

    **Déroulement :**
    1. Recherche l'utilisateur correspondant à l'identifiant saisi.
    2. Vérifie la correspondance du mot de passe avec le hash stocké.
    3. Calcule la date d'expiration du token.
    4. Génère et retourne un token JWT signé contenant l'ID utilisateur dans le claim `sub`.

    **Erreurs possibles :**
    - `401 UNAUTHORIZED` : Si l'e-mail n'existe pas ou si le mot de passe est incorrect.
    """
    # 1. Recherche de l'utilisateur par e-mail (champ 'username' du formulaire OAuth2)
    result = await session.execute(select(User).where(User.email == form_data.username))
    user = result.scalars().first()
    
    # 2. Contrôle de sécurité : existence et vérification du mot de passe
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou mot de passe incorrect.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # 3. Calcul de la durée de validité du jeton
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    # 4. Création du jeton JWT
    access_token = create_access_token(
        data={"sub": str(user.id)},
        expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}


@router.get(
    "/me", 
    response_model=UserRead,
    summary="Récupération du profil de l'utilisateur connecté",
    response_description="Les informations publiques du compte authentifié."
)
def get_me(current_user: Annotated[User, Depends(get_current_user)]):
    """
    Retourne les informations du compte actuellement authentifié.

    - **current_user**: Utilisateur injecté automatiquement via la dépendance JWT `get_current_user`.

    **Déroulement :**
    - Intercepte le token JWT transmis dans le header `Authorization: Bearer <token>`.
    - Si le token est valide et l'utilisateur identifié, renvoie son profil au format `UserPublic`.

    **Erreurs possibles :**
    - `401 UNAUTHORIZED` : Si le token JWT est absent, expiré, invalide ou falsifié.
    """
    return current_user