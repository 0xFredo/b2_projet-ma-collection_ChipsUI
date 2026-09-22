from datetime import datetime
from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship

from models.collection import CollectionEntry

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True)
    hashed_password: str
    role: str = Field(default="user") # "user" ou "admin"
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Relation vers la collection personnelle
    collection_entries: List["CollectionEntry"] = Relationship(back_populates="user", sa_relationship_kwargs={"cascade": "all, delete-orphan"})
