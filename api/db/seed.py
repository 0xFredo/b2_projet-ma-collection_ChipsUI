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
from core.security import get_password_hash

# Tableau de données du catalogue (à remplacer/compléter selon l'univers choisi)
ITEMS_DATA = [
    # --- Catégorie 1: Ondulées ---
    {"titre": "Brets Poulet Rôti", "categorie": "Ondulées", "description": "Les fameuses chips ondulées au goût de poulet dominical.", "annee": 1995, "image_url": "https://cms.brets.fr/app/uploads/2026/01/poulet-braise-1.png", "saveur": "Poulet Rôti", "marque": "Brets"},
    {"titre": "Brets Cevennes", "categorie": "Ondulées", "description": "Chips ondulées aux oignons doux des Cévennes.", "annee": 2012, "image_url": "https://www.myamericanshop.com/cdn/shop/files/brets-flavour-auvergne-aop-3497917003540-1155387765.png?v=1784218386", "saveur": "Oignon doux", "marque": "Brets"},
    {"titre": "Lay's Ondulées Onctueuse", "categorie": "Ondulées", "description": "Chips ondulées à la texture croustillante et saveur crème.", "annee": 2005, "image_url": "https://media.carrefour.fr/media/referential/media/29f1b22bf25e4292b61700007041fdbe/p_540x540/03168930179696_H1N1_s03.jpeg", "saveur": "Crème fraîche", "marque": "Lay's"},
    {"titre": "Ruffles Barbecue", "categorie": "Ondulées", "description": "Grosses ondulations américaines au goût fumé.", "annee": 1958, "image_url": "https://americanuncleshop.fr/cdn/shop/products/ruffles-barbecue-30g.jpg?v=1668414181&width=1080", "saveur": "Barbecue", "marque": "Ruffles"},
    {"titre": "Vico Ondulées Sel", "categorie": "Ondulées", "description": "Classique français croustillant salé au sel de Guérande.", "annee": 1955, "image_url": "https://fridg-front.s3.amazonaws.com/media/CACHE/images/products/chips-ondulees-salee-vico-135-g/ac15d663e65882c277883968b70d408f.jpg", "saveur": "Nature", "marque": "Vico"},
    {"titre": "Brets Camembert", "categorie": "Ondulées", "description": "Goût typique du fromage normand en chips.", "annee": 2018, "image_url": "https://media.carrefour.fr/media/referential/media/96f1af21c8024eb2859514af71d62519/p_1500x1500/03497917001928_A1N1_s01.png", "saveur": "Camembert", "marque": "Brets"},
    {"titre": "Lay's Max Cheeseburger", "categorie": "Ondulées", "description": "Ondulations profondes au goût de burger garni.", "annee": 2020, "image_url": "https://images.openfoodfacts.org/images/products/316/893/015/5966/front_fr.30.full.jpg", "saveur": "Cheeseburger", "marque": "Lay's"},
    {"titre": "Brets Chèvre Piment d'Espelette", "categorie": "Ondulées", "description": "Mariage du fromage de chèvre et de la chaleur du piment.", "annee": 2015, "image_url": "https://media.carrefour.fr/media/referential/media/b8a4ec69223241f0978059bc26ab0198/p_540x540/03497917000518_A1N1_s01.png", "saveur": "Chèvre Piment", "marque": "Brets"},
    {"titre": "Ruffles Cheddar Sour Cream", "categorie": "Ondulées", "description": "Saveur américaine intense au cheddar et crème sûre.", "annee": 1980, "image_url": "https://americanuncleshop.fr/cdn/shop/files/ruffles-cheddar-sour-cream.jpg?v=1715176434", "saveur": "Cheddar Crème", "marque": "Ruffles"},
    {"titre": "Vico Ondulées Pickle", "categorie": "Ondulées", "description": "Une touche d'acidité et de piquant avec le cornichon.", "annee": 2021, "image_url": "https://www.maximo.fr/media/image/56/ff/e7e7dde2268ae9b75f374894efc8.jpg", "saveur": "Cornichon", "marque": "Vico"},

    # --- Catégorie 2: Cuites au chaudron ---
    {"titre": "Tyrrells Sea Salt & Cider Vinegar", "categorie": "Cuites au chaudron", "description": "Chips anglaises avec un vinaigre de cidre corsé.", "annee": 2002, "image_url": "https://www.tyrrellscrisps.fr/wp-content/uploads/2017/07/Tyrrells-International-Sea-Salt-Cider-Vinegar-150g.png", "saveur": "Vinaigre de cidre", "marque": "Tyrrells"},
    {"titre": "Kettle Brand Honey Dijon", "categorie": "Cuites au chaudron", "description": "Cuisson lente artisanale, saveur moutarde douce et miel.", "annee": 1982, "image_url": "https://cloudinary.images-iherb.com/image/upload/f_auto,q_auto:eco/images/ktt/ktt03070/y/26.jpg", "saveur": "Moutarde Miel", "marque": "Kettle"},
    {"titre": "Tyrrells Black Pepper", "categorie": "Cuites au chaudron", "description": "Sel marin et poivre noir concassé au chaudron.", "annee": 2004, "image_url": "https://www.tyrrellscrisps.fr/wp-content/uploads/2017/07/Tyrrells-International-Sea-Salt-Black-Pepper-150g.png", "saveur": "Poivre Noir", "marque": "Tyrrells"},
    {"titre": "Lay's Paysanne Nature", "categorie": "Cuites au chaudron", "description": "Tranches épaisses cuites doucement pour un extra croustillant.", "annee": 2010, "image_url": "https://www.lays.fr/prod/s3fs-public/2025-11/3168930168133%20-%20Lay%27s%20Paysannes%20Nature%20155g.png", "saveur": "Nature Salée", "marque": "Lay's"},
    {"titre": "Kettle Sea Salt & Balsamic", "categorie": "Cuites au chaudron", "description": "Vinaigre balsamique de Modène et sel marin.", "annee": 1998, "image_url": "https://m.media-amazon.com/images/I/51iLhC9lxVL.jpg", "saveur": "Balsamique", "marque": "Kettle"},
    {"titre": "Sibell Truffe Noire", "categorie": "Cuites au chaudron", "description": "Chips artisanales provençales aromatisées à la truffe.", "annee": 2016, "image_url": "https://images.openfoodfacts.org/images/products/339/611/500/0200/front_fr.62.full.jpg", "saveur": "Truffe Noire", "marque": "Sibell"},
    {"titre": "Tyrrells Sweet Chilli", "categorie": "Cuites au chaudron", "description": "Piment doux asiatique et note de rouge sucré.", "annee": 2008, "image_url": "https://www.tyrrellscrisps.fr/wp-content/uploads/2017/07/Tyrrells-International-Sweet-Chilli-Red-Pepper-150g.png", "saveur": "Piment Doux", "marque": "Tyrrells"},
    {"titre": "Kettle Jalapeño", "categorie": "Cuites au chaudron", "description": "Piment jalapeño mexicain pour amateurs de sensations pimentées.", "annee": 2005, "image_url": "https://i.ebayimg.com/images/g/UAYAAOSw7rJjENoX/s-l400.jpg", "saveur": "Jalapeño", "marque": "Kettle"},
    {"titre": "Sibell Ail et Romarin", "categorie": "Cuites au chaudron", "description": "Saveurs méditerranéennes infusées à la cuisson.", "annee": 2019, "image_url": "https://media.carrefour.fr/medias/52db10efb91c3d2aa9362a7698498d35/p_1500x1500/3396118129106-photosite-20161118-162803-0.jpg", "saveur": "Ail Romarin", "marque": "Sibell"},
    {"titre": "Tyrrells Smoked Paprika", "categorie": "Cuites au chaudron", "description": "Paprika fumé au bois de chêne.", "annee": 2014, "image_url": "https://www.tyrrellscrisps.fr/wp-content/uploads/2024/04/smoked-paprika.png", "saveur": "Paprika Fumé", "marque": "Tyrrells"},

    # --- Catégorie 3: Tuiles ---
    {"titre": "Pringles Sour Cream & Onion", "categorie": "Tuiles", "description": "Les tuiles iconiques au goût crème sûre et oignon.", "annee": 1968, "image_url": "https://cdn.auchan.fr/media/P02000000000IPAPRIMARY_0x0/B2CD/?width=1024&height=1024&fit=pad&format=rw&quality=75", "saveur": "Crème Oignon", "marque": "Pringles"},
    {"titre": "Pringles Original", "categorie": "Tuiles", "description": "La tuile salée originale en tube paraboloïde.", "annee": 1967, "image_url": "https://cdn.auchan.fr/media/P02000000000IP9PRIMARY_0x0/B2CD/?width=1024&height=1024&fit=pad&format=rw&quality=75", "saveur": "Nature", "marque": "Pringles"},
    {"titre": "Pringles Paprika", "categorie": "Tuiles", "description": "Saveur paprika épicée très populaire en Europe.", "annee": 1992, "image_url": "https://cdn.auchan.fr/media/P02000000001ADCPRIMARY_0x0/B2CD/?width=1024&height=1024&fit=pad&format=rw&quality=75", "saveur": "Paprika", "marque": "Pringles"},
    {"titre": "Lay's Stax Original", "categorie": "Tuiles", "description": "Tuiles de pomme de terre croustillantes en boîte rigide.", "annee": 2003, "image_url": "https://www.tastyrewards.com/sites/default/files/2026-02/271-PRODUCT-SHOT-984x983-STAX-CLASSIC.png", "saveur": "Nature", "marque": "Lay's"},
    {"titre": "Pringles Texas BBQ Sauce", "categorie": "Tuiles", "description": "Goût de sauce barbecue sucrée et fumée.", "annee": 1995, "image_url": "https://cdn.auchan.fr/media/P02000000001AM1PRIMARY_0x0/B2CD/?width=1024&height=1024&fit=pad&format=rw&quality=75", "saveur": "Barbecue Texas", "marque": "Pringles"},
    {"titre": "Lay's Stax Sour Cream & Onion", "categorie": "Tuiles", "description": "Alternative Lay's en format tuiles empilées.", "annee": 2004, "image_url": "https://popsamerica.com/13270-large_default/lay-s-stax-sour-cream-onion.jpg", "saveur": "Crème Oignon", "marque": "Lay's"},
    {"titre": "Pringles Hot & Spicy", "categorie": "Tuiles", "description": "Mélange d'épices fortes pour un piquant immédiat.", "annee": 2000, "image_url": "https://cdn.auchan.fr/media/P02000000000IPBPRIMARY_0x0/B2CD/?width=1024&height=1024&fit=pad&format=rw&quality=75", "saveur": "Épicé", "marque": "Pringles"},
    {"titre": "Pringles Salt & Vinegar", "categorie": "Tuiles", "description": "L'acidité vive du vinaigre en format tuile.", "annee": 1985, "image_url": "https://cdn.auchan.fr/media/A0220170322000680382PRIMARY_0x0/B2CD/?width=1024&height=1024&fit=pad&format=rw&quality=75", "saveur": "Vinaigre", "marque": "Pringles"},
    {"titre": "Pringles Emmental", "categorie": "Tuiles", "description": "Tuiles gourmandes au goût d'emmental fondu.", "annee": 2011, "image_url": "https://azseller.s3.amazonaws.com/5fde132ca9cc36749c65b7c4/items/b24b7483-1aa8-448c-b45e-c48c90f05ad4/1200/eabb86cd-00a6-4451-b1f2-839bc92aa389.jpg", "saveur": "Emmental", "marque": "Pringles"},
    {"titre": "Lay's Stax Cheddar", "categorie": "Tuiles", "description": "Tuiles recouvertes d'une fine poudre de fromage cheddar.", "annee": 2006, "image_url": "https://popsamerica.com/13266-large_default/lay-s-stax-cheddar.jpg", "saveur": "Cheddar", "marque": "Lay's"},

    # --- Catégorie 4: Tortillas ---
    {"titre": "Doritos Nacho Cheese", "categorie": "Tortillas", "description": "Triangles de maïs croustillants au fromage nacho.", "annee": 1974, "image_url": "https://www.doritos.fr/prod/s3fs-public/2024-03/mockup-Doritos-nacho-cheese-160g.png", "saveur": "Fromage Nacho", "marque": "Doritos"},
    {"titre": "Doritos Cool Ranch", "categorie": "Tortillas", "description": "Saveur emblématique américaine herbes et ail doux.", "annee": 1986, "image_url": "https://m.media-amazon.com/images/I/81po0-JdVxL._AC_UF894,1000_QL80_.jpg", "saveur": "Ranch", "marque": "Doritos"},
    {"titre": "Doritos Sweet Chilli Pepper", "categorie": "Tortillas", "description": "Piment doux sucré-salé sur base de maïs grillé.", "annee": 2008, "image_url": "https://shop-fr.selecta.com/cdn/shop/files/I0003956_DORITOSSWEETCHILI44G_1500x.png?v=1775656135", "saveur": "Piment Doux", "marque": "Doritos"},
    {"titre": "Old El Paso Tortilla Salted", "categorie": "Tortillas", "description": "Chips de maïs mexicaines parfaites à tremper dans le guacamole.", "annee": 1938, "image_url": "https://media.carrefour.fr/media/referential/media/19ad6f365b404519bf4984e83e714c5c/p_1500x1500/08410076483355_C1N1_s02.jpeg", "saveur": "Sel Marin", "marque": "Old El Paso"},
    {"titre": "Takis Fuego", "categorie": "Tortillas", "description": "Tortillas roulées ultra pimentées au piment et citron vert.", "annee": 1999, "image_url": "https://i.ebayimg.com/images/g/n5cAAeSwvCVpcq-4/s-l1200.jpg", "saveur": "Piment Citron", "marque": "Takis"},
    {"titre": "Doritos Chilli Heatwave", "categorie": "Tortillas", "description": "Intense piment rouge pour amateurs de sensations fortes.", "annee": 2002, "image_url": "https://m.media-amazon.com/images/I/61muRPln0-L.jpg", "saveur": "Piment Fort", "marque": "Doritos"},
    {"titre": "Old El Paso Chilli Tortilla", "categorie": "Tortillas", "description": "Chips tortillas parfumées aux épices mexicaines.", "annee": 1995, "image_url": "https://m.media-amazon.com/images/I/71xg62KKYpL.jpg", "saveur": "Épices Tex-Mex", "marque": "Old El Paso"},
    {"titre": "Takis Blue Heat", "categorie": "Tortillas", "description": "Tortillas roulées bleues extrêmement piquantes.", "annee": 2019, "image_url": "https://media.carrefour.fr/media/referential/media/9c9ede99a3ef420c8c97341967c4457e/p_1500x1500/08412600047484_A1N1_s01.png", "saveur": "Piment Intense", "marque": "Takis"},
    {"titre": "Doritos Sizzlin' Barbecue", "categorie": "Tortillas", "description": "Goût barbecue grillé intense sur tortilla dorée.", "annee": 2021, "image_url": "https://m.media-amazon.com/images/I/71ALLDnv1xL.jpg", "saveur": "Barbecue Grillé", "marque": "Doritos"},
    {"titre": "Santitas Tortilla Strips", "categorie": "Tortillas", "description": "Bandelettes de tortillas traditionnelles au maïs blanc.", "annee": 1989, "image_url": "https://d2lnr5mha7bycj.cloudfront.net/product-image/file/large_49abc48d-0e1c-4415-b6b0-46314c11ccfa.png", "saveur": "Maïs Blanc", "marque": "Santitas"}
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

        # 2. Création du compte de test (optionnel mais pratique)
        test_email = "test@example.com"
        stmt_user = select(User).where(User.email == test_email)
        existing_user = (await session.execute(stmt_user)).scalar_one_or_none()

        if not existing_user:
            demo_user = User(
                email=test_email,
                hashed_password=get_password_hash("password123"),
            )
            session.add(demo_user)
            print(f"Utilisateur de test créé : {test_email}")
        else:
            print(f"Utilisateur déjà présent : {test_email}")

        # Validation de la transaction
        await session.commit()
        print(f"Peuplement terminé ! ({added_count} éléments ajoutés)")


if __name__ == "__main__":
    asyncio.run(seed_database())