# Modèle SQLModel/SQLAlchemy pour le catalogue

from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship

from models.collection import CollectionEntry

class Item(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(index=True)
    description: str
    category: str = Field(index=True)
    image_url: str
    
    # 1 à 2 champs spécifiques à ton univers (ex: Livre)
    author: str
    year: int

    # Relation vers les entrées de collection
    collection_entries: List["CollectionEntry"] = Relationship(back_populates="item", sa_relationship_kwargs={"cascade": "all, delete-orphan"})
