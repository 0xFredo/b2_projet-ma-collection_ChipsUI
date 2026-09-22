# Modèle pour l'entrée de collection

from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field, Relationship

from models.user import User
from models.item import Item

class CollectionEntry(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    item_id: int = Field(foreign_key="item.id")
    
    status: str = Field(default="a_decouvrir") # "a_decouvrir", "en_cours", "termine"
    rating: Optional[int] = Field(default=None) # 1 à 5
    comment: Optional[str] = Field(default=None)
    updated_at: datetime = Field(default_factory=datetime.utcnow, sa_column_kwargs={"onupdate": datetime.utcnow})

    # Relations
    user: Optional["User"] = Relationship(back_populates="collection_entries")
    item: Optional["Item"] = Relationship(back_populates="collection_entries")
