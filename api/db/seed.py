# Script de peuplement (40+ items)

import asyncio
from sqlmodel import select
from db.database import AsyncSessionLocal
from models.item import Item # Adapte selon ton arborescence

ITEMS_DATA = [ # METTRE ICI ITEMS PAR DEFAUT
    {"title": "Item 1", "description": "Description de l'item 1", "price": 10.0},
]

async def seed_database():
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
