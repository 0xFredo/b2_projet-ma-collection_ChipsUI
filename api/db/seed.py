# Script de peuplement (test avec 1 item)
import asyncio
from sqlmodel import select

from db.database import AsyncSessionLocal, init_db
from models.item import Item
from models.collection import CollectionEntry  # <-- OBLIGATOIRE pour charger la relation
from models.user import User                   # <-- OBLIGATOIRE pour charger la relation

# Remplacez / complétez ce tableau dès que vous avez choisi votre univers !
ITEMS_DATA = [
    {
        "titre": "Item de Test 1",
        "description": "Description de l'élément de test pour vérifier la BDD",
        "categorie": "Général",
        "image_url": "https://picsum.photos/seed/test/200/300",
        "auteur": "Auteur Test",
        "annee": 2026,
    },
]


async def seed_database():
    await init_db()

    async with AsyncSessionLocal() as session:
        print("🌱 Début du peuplement de la base de données...")
        
        added_count = 0
        for data in ITEMS_DATA:
            statement = select(Item).where(Item.titre == data["titre"])
            result = await session.execute(statement)
            existing_item = result.scalar_one_or_none()
            
            if not existing_item:
                new_item = Item(**data)
                session.add(new_item)
                added_count += 1
                print(f"➕ Ajout : {data['titre']}")
            else:
                print(f"⏩ Déjà présent : {data['titre']}")
                
        await session.commit()
        print(f"✅ Peuplement terminé ! ({added_count} éléments ajoutés)")

if __name__ == "__main__":
    asyncio.run(seed_database())