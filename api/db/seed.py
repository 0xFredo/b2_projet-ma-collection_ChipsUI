"""
Script d'initialisation et de peuplement de la base de données.
Permet d'insérer les éléments du catalogue de manière idempotente (anti-doublon).
"""

import asyncio
from sqlmodel import select

from db.database import AsyncSessionLocal, init_db
from models.item import Item
from models.collection import CollectionEntry  # Imports nécessaires pour la résolution
from models.user import User  # des relations SQLModel / SQLAlchemy (noqa: F401)

# Tableau de données du catalogue (à remplacer/compléter selon l'univers choisi)
ITEMS_DATA = [
    # --- Catégorie 1: Ondulées ---
    {"titre": "Brets Poulet Rôti", "categorie": "Ondulées", "description": "Les fameuses chips ondulées au goût de poulet dominical.", "annee": 1995, "image_url": "https://cms.brets.fr/app/uploads/2026/01/poulet-braise-1.png", "saveur": "Poulet Rôti", "marque": "Brets"},
    {"titre": "Brets Cevennes", "categorie": "Ondulées", "description": "Chips ondulées aux oignons doux des Cévennes.", "annee": 2012, "image_url": "https://www.myamericanshop.com/cdn/shop/files/brets-flavour-auvergne-aop-3497917003540-1155387765.png?v=1784218386", "saveur": "Oignon doux", "marque": "Brets"},
    {"titre": "Lay's Ondulées Onctueuse", "categorie": "Ondulées", "description": "Chips ondulées à la texture croustillante et saveur crème.", "annee": 2005, "image_url": "https://picsum.photos/seed/lays1/400/600", "saveur": "Crème fraîche", "marque": "Lay's"},
    {"titre": "Ruffles Barbecue", "categorie": "Ondulées", "description": "Grosses ondulations américaines au goût fumé.", "annee": 1958, "image_url": "https://picsum.photos/seed/ruffles1/400/600", "saveur": "Barbecue", "marque": "Ruffles"},
    {"titre": "Vico Ondulées Sel", "categorie": "Ondulées", "description": "Classique français croustillant salé au sel de Guérande.", "annee": 1955, "image_url": "https://picsum.photos/seed/vico1/400/600", "saveur": "Nature", "marque": "Vico"},
    {"titre": "Brets Camembert", "categorie": "Ondulées", "description": "Goût typique du fromage normand en chips.", "annee": 2018, "image_url": "https://picsum.photos/seed/brets3/400/600", "saveur": "Camembert", "marque": "Brets"},
    {"titre": "Lay's Max Cheeseburger", "categorie": "Ondulées", "description": "Ondulations profondes au goût de burger garni.", "annee": 2020, "image_url": "https://picsum.photos/seed/lays2/400/600", "saveur": "Cheeseburger", "marque": "Lay's"},
    {"titre": "Brets Chèvre Piment d'Espelette", "categorie": "Ondulées", "description": "Mariage du fromage de chèvre et de la chaleur du piment.", "annee": 2015, "image_url": "https://picsum.photos/seed/brets4/400/600", "saveur": "Chèvre Piment", "marque": "Brets"},
    {"titre": "Ruffles Cheddar Sour Cream", "categorie": "Ondulées", "description": "Saveur américaine intense au cheddar et crème sûre.", "annee": 1980, "image_url": "https://picsum.photos/seed/ruffles2/400/600", "saveur": "Cheddar Crème", "marque": "Ruffles"},
    {"titre": "Vico Ondulées Pickle", "categorie": "Ondulées", "description": "Une touche d'acidité et de piquant avec le cornichon.", "annee": 2021, "image_url": "https://picsum.photos/seed/vico2/400/600", "saveur": "Cornichon", "marque": "Vico"},

    # --- Catégorie 2: Cuites au chaudron ---
    {"titre": "Tyrrells Sea Salt & Cider Vinegar", "categorie": "Cuites au chaudron", "description": "Chips anglaises avec un vinaigre de cidre corsé.", "annee": 2002, "image_url": "https://picsum.photos/seed/tyrrells1/400/600", "saveur": "Vinaigre de cidre", "marque": "Tyrrells"},
    {"titre": "Kettle Brand Honey Dijon", "categorie": "Cuites au chaudron", "description": "Cuisson lente artisanale, saveur moutarde douce et miel.", "annee": 1982, "image_url": "https://picsum.photos/seed/kettle1/400/600", "saveur": "Moutarde Miel", "marque": "Kettle"},
    {"titre": "Tyrrells Black Pepper", "categorie": "Cuites au chaudron", "description": "Sel marin et poivre noir concassé au chaudron.", "annee": 2004, "image_url": "https://picsum.photos/seed/tyrrells2/400/600", "saveur": "Poivre Noir", "marque": "Tyrrells"},
    {"titre": "Lay's Paysanne Nature", "categorie": "Cuites au chaudron", "description": "Tranches épaisses cuites doucement pour un extra croustillant.", "annee": 2010, "image_url": "https://picsum.photos/seed/lays3/400/600", "saveur": "Nature Salée", "marque": "Lay's"},
    {"titre": "Kettle Sea Salt & Balsamic", "categorie": "Cuites au chaudron", "description": "Vinaigre balsamique de Modène et sel marin.", "annee": 1998, "image_url": "https://picsum.photos/seed/kettle2/400/600", "saveur": "Balsamique", "marque": "Kettle"},
    {"titre": "Sibell Truffe Noire", "categorie": "Cuites au chaudron", "description": "Chips artisanales provençales aromatisées à la truffe.", "annee": 2016, "image_url": "https://picsum.photos/seed/sibell1/400/600", "saveur": "Truffe Noire", "marque": "Sibell"},
    {"titre": "Tyrrells Sweet Chilli", "categorie": "Cuites au chaudron", "description": "Piment doux asiatique et note de rouge sucré.", "annee": 2008, "image_url": "https://picsum.photos/seed/tyrrells3/400/600", "saveur": "Piment Doux", "marque": "Tyrrells"},
    {"titre": "Kettle Jalapeño", "categorie": "Cuites au chaudron", "description": "Piment jalapeño mexicain pour amateurs de sensations pimentées.", "annee": 2005, "image_url": "https://picsum.photos/seed/kettle3/400/600", "saveur": "Jalapeño", "marque": "Kettle"},
    {"titre": "Sibell Ail et Romarin", "categorie": "Cuites au chaudron", "description": "Saveurs méditerranéennes infusées à la cuisson.", "annee": 2019, "image_url": "https://picsum.photos/seed/sibell2/400/600", "saveur": "Ail Romarin", "marque": "Sibell"},
    {"titre": "Tyrrells Smoked Paprika", "categorie": "Cuites au chaudron", "description": "Paprika fumé au bois de chêne.", "annee": 2014, "image_url": "https://picsum.photos/seed/tyrrells4/400/600", "saveur": "Paprika Fumé", "marque": "Tyrrells"},

    # --- Catégorie 3: Tuiles ---
    {"titre": "Pringles Sour Cream & Onion", "categorie": "Tuiles", "description": "Les tuiles iconiques au goût crème sûre et oignon.", "annee": 1968, "image_url": "https://picsum.photos/seed/pringles1/400/600", "saveur": "Crème Oignon", "marque": "Pringles"},
    {"titre": "Pringles Original", "categorie": "Tuiles", "description": "La tuile salée originale en tube paraboloïde.", "annee": 1967, "image_url": "https://picsum.photos/seed/pringles2/400/600", "saveur": "Nature", "marque": "Pringles"},
    {"titre": "Pringles Paprika", "categorie": "Tuiles", "description": "Saveur paprika épicée très populaire en Europe.", "annee": 1992, "image_url": "https://picsum.photos/seed/pringles3/400/600", "saveur": "Paprika", "marque": "Pringles"},
    {"titre": "Lay's Stax Original", "categorie": "Tuiles", "description": "Tuiles de pomme de terre croustillantes en boîte rigide.", "annee": 2003, "image_url": "https://picsum.photos/seed/stax1/400/600", "saveur": "Nature", "marque": "Lay's"},
    {"titre": "Pringles Texas BBQ Sauce", "categorie": "Tuiles", "description": "Goût de sauce barbecue sucrée et fumée.", "annee": 1995, "image_url": "https://picsum.photos/seed/pringles4/400/600", "saveur": "Barbecue Texas", "marque": "Pringles"},
    {"titre": "Lay's Stax Sour Cream & Onion", "categorie": "Tuiles", "description": "Alternative Lay's en format tuiles empilées.", "annee": 2004, "image_url": "https://picsum.photos/seed/stax2/400/600", "saveur": "Crème Oignon", "marque": "Lay's"},
    {"titre": "Pringles Hot & Spicy", "categorie": "Tuiles", "description": "Mélange d'épices fortes pour un piquant immédiat.", "annee": 2000, "image_url": "https://picsum.photos/seed/pringles5/400/600", "saveur": "Épicé", "marque": "Pringles"},
    {"titre": "Pringles Salt & Vinegar", "categorie": "Tuiles", "description": "L'acidité vive du vinaigre en format tuile.", "annee": 1985, "image_url": "https://picsum.photos/seed/pringles6/400/600", "saveur": "Vinaigre", "marque": "Pringles"},
    {"titre": "Pringles Emmental", "categorie": "Tuiles", "description": "Tuiles gourmandes au goût d'emmental fondu.", "annee": 2011, "image_url": "https://picsum.photos/seed/pringles7/400/600", "saveur": "Emmental", "marque": "Pringles"},
    {"titre": "Lay's Stax Cheddar", "categorie": "Tuiles", "description": "Tuiles recouvertes d'une fine poudre de fromage cheddar.", "annee": 2006, "image_url": "https://picsum.photos/seed/stax3/400/600", "saveur": "Cheddar", "marque": "Lay's"},

    # --- Catégorie 4: Tortillas ---
    {"titre": "Doritos Nacho Cheese", "categorie": "Tortillas", "description": "Triangles de maïs croustillants au fromage nacho.", "annee": 1974, "image_url": "https://picsum.photos/seed/doritos1/400/600", "saveur": "Fromage Nacho", "marque": "Doritos"},
    {"titre": "Doritos Cool Ranch", "categorie": "Tortillas", "description": "Saveur emblématique américaine herbes et ail doux.", "annee": 1986, "image_url": "https://picsum.photos/seed/doritos2/400/600", "saveur": "Ranch", "marque": "Doritos"},
    {"titre": "Doritos Sweet Chilli Pepper", "categorie": "Tortillas", "description": "Piment doux sucré-salé sur base de maïs grillé.", "annee": 2008, "image_url": "https://picsum.photos/seed/doritos3/400/600", "saveur": "Piment Doux", "marque": "Doritos"},
    {"titre": "Old El Paso Tortilla Salted", "categorie": "Tortillas", "description": "Chips de maïs mexicaines parfaites à tremper dans le guacamole.", "annee": 1938, "image_url": "https://picsum.photos/seed/oldelpaso1/400/600", "saveur": "Sel Marin", "marque": "Old El Paso"},
    {"titre": "Takis Fuego", "categorie": "Tortillas", "description": "Tortillas roulées ultra pimentées au piment et citron vert.", "annee": 1999, "image_url": "https://picsum.photos/seed/takis1/400/600", "saveur": "Piment Citron", "marque": "Takis"},
    {"titre": "Doritos Chilli Heatwave", "categorie": "Tortillas", "description": "Intense piment rouge pour amateurs de sensations fortes.", "annee": 2002, "image_url": "https://picsum.photos/seed/doritos4/400/600", "saveur": "Piment Fort", "marque": "Doritos"},
    {"titre": "Old El Paso Chilli Tortilla", "categorie": "Tortillas", "description": "Chips tortillas parfumées aux épices mexicaines.", "annee": 1995, "image_url": "https://picsum.photos/seed/oldelpaso2/400/600", "saveur": "Épices Tex-Mex", "marque": "Old El Paso"},
    {"titre": "Takis Blue Heat", "categorie": "Tortillas", "description": "Tortillas roulées bleues extrêmement piquantes.", "annee": 2019, "image_url": "https://picsum.photos/seed/takis2/400/600", "saveur": "Piment Intense", "marque": "Takis"},
    {"titre": "Doritos Sizzlin' Barbecue", "categorie": "Tortillas", "description": "Goût barbecue grillé intense sur tortilla dorée.", "annee": 2021, "image_url": "https://picsum.photos/seed/doritos5/400/600", "saveur": "Barbecue Grillé", "marque": "Doritos"},
    {"titre": "Santitas Tortilla Strips", "categorie": "Tortillas", "description": "Bandelettes de tortillas traditionnelles au maïs blanc.", "annee": 1989, "image_url": "https://picsum.photos/seed/santitas1/400/600", "saveur": "Maïs Blanc", "marque": "Santitas"}
]


async def seed_database() -> None:
    """
    Initialise les tables en base de données et insère les données de test
    si elles n'existent pas déjà (évite les doublons lors des re-exécutions).
    """
    # Création des tables si elles n'existent pas
    await init_db()

    async with AsyncSessionLocal() as session:
        print("Début du peuplement de la base de données...")

        added_count = 0
        for data in ITEMS_DATA:
            # Vérification de l'existence de l'élément par son titre
            statement = select(Item).where(Item.titre == data["titre"])
            result = await session.execute(statement)
            existing_item = result.scalar_one_or_none()

            # Insertion uniquement si l'item n'existe pas en base
            if not existing_item:
                new_item = Item(**data)
                session.add(new_item)
                added_count += 1
                print(f"Ajout : {data['titre']}")
            else:
                print(f"Déjà présent : {data['titre']}")

        # Validation de la transaction
        await session.commit()
        print(f"Peuplement terminé ! ({added_count} éléments ajoutés)")


if __name__ == "__main__":
    asyncio.run(seed_database())