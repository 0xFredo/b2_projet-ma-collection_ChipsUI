# Modèle SQLModel pour le catalogue (Livres / Recettes / Jeux)

from typing import TYPE_CHECKING, Optional, List
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from models.collection import CollectionEntry

class Item(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    titre: str = Field(index=True)
    description: str
    categorie: str = Field(index=True)
    annee: int
    image_url: str
    
    # 2 champs propres à l'univers
    saveur: str
    marque: str

    # Relation vers les entrées de collection
    collection_entries: List["CollectionEntry"] = Relationship(
        back_populates="item", 
        sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )