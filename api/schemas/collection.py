"""Schémas Pydantic pour la gestion de la Collection personnelle et des statistiques."""

from datetime import datetime
from typing import Literal
from pydantic import BaseModel, ConfigDict, Field
from schemas.item import ItemRead

# Type littéral restreint aux trois statuts autorisés par le contrat d'API
StatutType = Literal["a_decouvrir", "en_cours", "termine"]

# Données requises pour l'ajout d'un élément à sa collection (POST /me/collection)
class CollectionEntryCreate(BaseModel):
    item_id: int
    statut: StatutType = "a_decouvrir"
    note: int | None = Field(None, ge=1, le=5)
    commentaire: str | None = None

# Données optionnelles pour la modification partielle d'une entrée (PATCH /me/collection/{entry_id})
class CollectionEntryUpdate(BaseModel):
    statut: StatutType | None = None
    note: int | None = Field(None, ge=1, le=5)
    commentaire: str | None = None

# Données renvoyées par l'API pour une entrée avec l'objet Item imbriqué
class CollectionEntryRead(BaseModel):
    id: int
    statut: StatutType
    note: int | None = Field(None, ge=1, le=5)
    commentaire: str | None = None
    date_ajout: datetime
    item: ItemRead # Modele Item récupéré

    model_config = ConfigDict(from_attributes=True)

# Structure de la réponse pour le tableau de bord (GET /me/stats)
class StatsResponse(BaseModel):
    total: int
    par_statut: dict[str, int] # Clef: statut (str), Valeur: quantité (int)
    note_moyenne: float | None = None