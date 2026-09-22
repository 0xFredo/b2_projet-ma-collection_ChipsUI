# Routes /me/*
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlmodel import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies.db import get_session
from dependencies.auth import get_current_user
from models.user import User
from models.item import Item
from models.collection import CollectionEntry
from schemas.collection import (
    CollectionEntryCreate,
    CollectionEntryUpdate,
    CollectionEntryRead,
    StatsResponse
)

router = APIRouter(prefix="/me", tags=["Collection Personnelle"])


@router.get("/collection", response_model=list[CollectionEntryRead])
async def get_my_collection(
    statut: Optional[str] = Query(default=None, description="Filtrer par statut (a_decouvrir, en_cours, termine)"),
    tri: Optional[str] = Query(default=None, description="Tri par 'date' ou 'note'"),
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """
    Récupère la collection personnelle de l'utilisateur connecté avec filtres et tri.
    """
    statement = (
        select(CollectionEntry)
        .where(CollectionEntry.user_id == current_user.id)
        .options(selectinload(CollectionEntry.item))
    )

    if statut:
        statement = statement.where(CollectionEntry.statut == statut)

    if tri == "date":
        statement = statement.order_by(CollectionEntry.date_ajout.desc())
    elif tri == "note":
        statement = statement.order_by(CollectionEntry.note.desc().nulls_last())

    result = await session.execute(statement)
    return result.scalars().all()


@router.post("/collection", response_model=CollectionEntryRead, status_code=status.HTTP_201_CREATED)
async def add_to_collection(
    entry_data: CollectionEntryCreate,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """
    Ajoute un élément du catalogue à la collection de l'utilisateur.
    """
    # 1. Vérifier si l'item existe dans le catalogue
    item_stmt = select(Item).where(Item.id == entry_data.item_id)
    item_res = await session.execute(item_stmt)
    item = item_res.scalar_one_or_none()

    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"erreur": {"code": 404, "message": "Item inexistant dans le catalogue"}}
        )

    # 2. Vérifier si l'item est déjà présent (409 Conflict)
    existing_stmt = select(CollectionEntry).where(
        CollectionEntry.user_id == current_user.id,
        CollectionEntry.item_id == entry_data.item_id
    )
    existing_res = await session.execute(existing_stmt)
    if existing_res.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={"erreur": {"code": 409, "message": "Élément déjà présent dans la collection"}}
        )

    # 3. Création de l'entrée
    new_entry = CollectionEntry(
        user_id=current_user.id,
        item_id=entry_data.item_id,
        statut=entry_data.statut,
        note=entry_data.note,
        commentaire=entry_data.commentaire
    )

    session.add(new_entry)
    await session.commit()

    # Charger la relation item pour la réponse
    res_stmt = (
        select(CollectionEntry)
        .where(CollectionEntry.id == new_entry.id)
        .options(selectinload(CollectionEntry.item))
    )
    res = await session.execute(res_stmt)
    return res.scalar_one()


@router.patch("/collection/{entry_id}", response_model=CollectionEntryRead)
async def update_collection_entry(
    entry_id: int,
    update_data: CollectionEntryUpdate,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """
    Met à jour une entrée de la collection (statut, note, commentaire).
    """
    statement = (
        select(CollectionEntry)
        .where(CollectionEntry.id == entry_id, CollectionEntry.user_id == current_user.id)
        .options(selectinload(CollectionEntry.item))
    )
    result = await session.execute(statement)
    entry = result.scalar_one_or_none()

    if not entry:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"erreur": {"code": 404, "message": "Entrée de collection introuvable"}}
        )

    data_dict = update_data.model_dump(exclude_unset=True)
    for key, value in data_dict.items():
        setattr(entry, key, value)

    session.add(entry)
    await session.commit()
    await session.refresh(entry)
    return entry


@router.delete("/collection/{entry_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_collection_entry(
    entry_id: int,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """
    Supprime un élément de la collection.
    """
    statement = select(CollectionEntry).where(
        CollectionEntry.id == entry_id,
        CollectionEntry.user_id == current_user.id
    )
    result = await session.execute(statement)
    entry = result.scalar_one_or_none()

    if not entry:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"erreur": {"code": 404, "message": "Entrée de collection introuvable"}}
        )

    await session.delete(entry)
    await session.commit()
    return None


@router.get("/stats", response_model=StatsResponse)
async def get_my_stats(
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """
    Renvoie le résumé des statistiques personnelles de l'utilisateur.
    """
    statement = select(CollectionEntry).where(CollectionEntry.user_id == current_user.id)
    result = await session.execute(statement)
    entries = result.scalars().all()

    total = len(entries)
    par_statut = {"a_decouvrir": 0, "en_cours": 0, "termine": 0}
    notes = []

    for e in entries:
        if e.statut in par_statut:
            par_statut[e.statut] += 1
        if e.note is not None:
            notes.append(e.note)

    note_moyenne = round(sum(notes) / len(notes), 2) if notes else None

    return StatsResponse(
        total=total,
        par_statut=par_statut,
        note_moyenne=note_moyenne
    )