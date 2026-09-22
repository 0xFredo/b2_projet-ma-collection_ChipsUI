# Script de peuplement (40+ items)

import asyncio
import sys
from pathlib import Path

from sqlmodel import select

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from db.database import AsyncSessionLocal
from db.database import init_db
from models.collection import CollectionEntry
from models.item import Item
from models.user import User

ITEMS_DATA = [ # METTRE ICI ITEMS PAR DEFAUT
    {
        "title": "Item 1",
        "description": "Description de l'item 1",
        "category": "general",
        "image_url": "",
        "author": "Auteur inconnu",
        "year": 2026,
    },
]

async def seed_database():
    await init_db()

    async with AsyncSessionLocal() as session:
        print("🌱 Début du peuplement de la base de données...")
        
        for data in ITEMS_DATA:
            # Vérifier si l'élément existe déjà pour éviter les doublons (via le titre)
            statement = select(Item).where(Item.title == data["title"])
            result = await session.execute(statement)
            existing_item = result.scalar_one_or_none()
            
            if not existing_item:
                new_item = Item(**data)
                session.add(new_item)
                print(f"➕ Ajout : {data['title']}")
            else:
                print(f"⏩ Déjà présent : {data['title']}")
                
        await session.commit()
        print("✅ Peuplement terminé avec succès !")

if __name__ == "__main__":
    asyncio.run(seed_database())
