# Routes /items/*
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlmodel import select, func, or_
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies.db import get_session
from models.item import Item
from schemas.item import ItemRead, ItemPaginatedResponse

router = APIRouter(prefix="/items", tags=["Catalogue"])


@router.get("", response_model=ItemPaginatedResponse)
async def get_items(
    q: Optional[str] = Query(default=None, min_length=1, description="Recherche par mot-clé (titre, description, auteur)"),
    categorie: Optional[str] = Query(default=None, description="Filtre par catégorie"),
    page: int = Query(default=1, ge=1, description="Numéro de la page (>= 1)"),
    limit: int = Query(default=12, ge=1, le=50, description="Nombre d'éléments par page (1 à 50)"),
    session: AsyncSession = Depends(get_session)
):
    """
    Récupère la liste des items du catalogue avec recherche, filtres et pagination.
    """
    statement = select(Item)

    # 1. Filtre par mot-clé (Recherche)
    if q:
        search_pattern = f"%{q}%"
        statement = statement.where(
            or_(
                Item.titre.ilike(search_pattern),
                Item.description.ilike(search_pattern),
                Item.auteur.ilike(search_pattern)
            )
        )

    # 2. Filtre par catégorie
    if categorie:
        statement = statement.where(Item.categorie == categorie)

    # 3. Calcul du total d'éléments
    count_statement = select(func.count()).select_from(statement.subquery())
    total_result = await session.execute(count_statement)
    total = total_result.scalar_one()

    # 4. Pagination
    offset = (page - 1) * limit
    paginated_statement = statement.offset(offset).limit(limit)
    
    result = await session.execute(paginated_statement)
    items = result.scalars().all()

    return ItemPaginatedResponse(
        total=total,
        page=page,
        limit=limit,
        results=items
    )


@router.get("/{item_id}", response_model=ItemRead)
async def get_item_by_id(
    item_id: int,
    session: AsyncSession = Depends(get_session)
):
    """
    Récupère la fiche détaillée d'un élément du catalogue.
    """
    statement = select(Item).where(Item.id == item_id)
    result = await session.execute(statement)
    item = result.scalar_one_or_none()

    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"erreur": {"code": 404, "message": f"Item {item_id} introuvable"}}
        )

    return item