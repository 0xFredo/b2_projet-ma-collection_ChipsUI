# Modèle pour la collection personnelle d'un utilisateur

from datetime import datetime, timezone
from typing import TYPE_CHECKING, Optional
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from models.item import Item
    from models.user import User

class CollectionEntry(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id", index=True)
    item_id: int = Field(foreign_key="item.id", index=True)
    
    statut: str = Field(default="a_decouvrir")  # "a_decouvrir", "en_cours", "termine"
    note: Optional[int] = Field(default=None)   # 1 à 5
    commentaire: Optional[str] = Field(default=None)
    date_ajout: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    # Relations
    user: Optional["User"] = Relationship(back_populates="collection_entries")
    item: Optional["Item"] = Relationship(back_populates="collection_entries")