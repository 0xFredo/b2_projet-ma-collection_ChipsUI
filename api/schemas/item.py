"""Schémas Pydantic pour la validation des données Item (Catalogue)."""

from pydantic import BaseModel, ConfigDict

# Structure de base commune à tous les objets du catalogue
class ItemBase(BaseModel):
    titre: str
    categorie: str
    description: str
    image_url: str | None = "" # Optionel
    annee: int
    auteur: str  # Champ spécifique univers Livres temporaire

# Données renvoyées par l'API pour un Item individuel (GET /items/{id})
class ItemRead(ItemBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

# Schéma pour la réponse paginée du GET /items
class ItemPaginatedResponse(BaseModel):
    total: int
    page: int
    limit: int
    results: list[ItemRead]