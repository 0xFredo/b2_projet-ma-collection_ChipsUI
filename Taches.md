✅ Florentin
✔️ Fredo
### **Phase 1 : Setup & Modèles de Données (Backend)**

1. **Initialiser l'environnement et l'arborescence**
    
    - Placer l'API dans le dossier `api/`. ✅
        
    - Créer le fichier `requirements.txt` (`fastapi`, `uvicorn`, `sqlmodel`, `aiosqlite`, `python-jose`, `passlib`, `pydantic-settings`). ✅
        
    - Configurer `core/config.py` pour charger les variables `.env` (ex: `SECRET_KEY`, `ALGORITHM`). ✅
        
2. **Configurer la base de données (`db/database.py`)**
    
    - Configurer le moteur SQLite asynchrone (`sqlite+aiosqlite://`).
        
    - Créer la fonction `get_db()` dans `dependencies/db.py` pour injecter la session BDD.
        
3. **Créer les modèles SQLModel / SQLAlchemy (`models/`)**
    
    - `User` : `id`, `email`, `hashed_password`, `role` (`user` ou `admin`), `created_at`.
        
    - `Item` : `id`, `title`, `description`, `category`, `image_url` + **1 à 2 champs spécifiques** à ton univers.
        
    - `CollectionEntry` : `id`, `user_id`, `item_id`, `status` (`a_decouvrir`, `en_cours`, `termine`), `rating` (1-5), `comment`, `updated_at`.
        
4. **Créer les schémas Pydantic (`schemas/`)**
    
    - Entrées/sorties pour l'authentification (`UserCreate`, `UserRead`, `Token`). ✅
        
    - Validation des entrées/sorties pour `Item` et `CollectionEntry`.
        

### **Phase 2 : Sécurité, Authentification & Seed (Backend)**

5. **Développer la sécurité (`core/security.py` & `dependencies/auth.py`)**
    
    - Hachage des mots de passe avec `bcrypt`.
        
    - Génération et vérification des tokens **JWT**.
        
    - Dépendance `get_current_user` pour vérifier la validité du token sur les routes protégées.
        
6. **Implémenter les routes `/auth/*` (`routers/auth.py`)**
    
    - `POST /auth/register` : Création de compte.
        
    - `POST /auth/login` : Authentification et retour du token JWT.
        
    - `GET /auth/me` : Récupération du profil connecté.
        
7. **Créer le script de peuplement (`db/seed.py`)**
    
    - Script permettant d'insérer au moins **40 éléments** dans la table `Item`.
        

### **Phase 3 : Métier, Collection & Stats (Backend)**

8. **Implémenter les routes du catalogue `/items/*` (`routers/items.py`)**
    
    - `GET /items` : Recherche, filtres par catégorie, pagination (`limit`/`offset`).
        
    - `GET /items/{id}` : Détail d'un élément.
        
    - `POST /items` : Ajout d'un élément (ouvert à tous ou restreint admin).
        
9. **Implémenter les routes utilisateur `/me/*` (`routers/collection.py`)**
    
    - `GET /me/collection` : Liste personnelle filtrable par statut (`a_decouvrir`, `en_cours`, `termine`).
        
    - `POST /me/collection` : Ajouter un item à sa collection.
        
    - `PUT /me/collection/{id}` : Modifier statut, note ou commentaire.
        
    - `DELETE /me/collection/{id}` : Retirer de sa collection.
        
    - `GET /me/stats` : Calculer le total d'items, la répartition par statut et la note moyenne.
        
10. **Finaliser `main.py` & CORS**
    
    - Assembler les routers.
        
    - Configurer le middleware **CORS** pour autoriser le frontend React.
        

### **Phase 4 : Frontend React & TypeScript**

11. **Setup React dans `web/`**
    
    - Initialiser Vite React + TypeScript, installer `react-router-dom` et les styles (CSS/Tailwind).
        
    - Créer le client HTTP centralisé dans `src/services/` (intercepteur de token JWT).
        
12. **Mettre en place les Contexts (`src/context/`)**
    
    - `AuthContext` : Gestion de la connexion, de la déconnexion et stockage du token.
        
    - `CollectionContext` : Gestion de l'état global de la collection utilisateur.
        
    - Custom Hook `useLocalStorage` générique.
        
13. **Développer les écrans principaux**
    
    - **Authentification** : Formulaires Login / Register.
        
    - **Catalogue** : Liste avec filtres, barre de recherche avec _debounce_, pagination.
        
    - **Ma Collection** : Tri par statut, modale de mise à jour (note/commentaire).
        
    - **Dashboard Stats** : Affichage graphique ou chiffré des statistiques personnelles.
        
14. **Soigner l'UI/UX**
    
    - Traiter les états : _chargement_, _erreur API_, _collection vide_.
        
    - Rendre le design responsive.
        

### **Phase 5 : Rendu & Finitions**

15. **Fusion Git & Nettoyage**
    
    - Fusionner la branche `fastapi` et la branche `React` sur `main`.
        
    - Vérifier l'arborescence finale :
        
        Plaintext
        
        ```
        / (racine)
        ├── api/
        ├── web/
        └── README.md
        ```
        
16. **Rédiger le `README.md`**
    
    - Instructions claires pour lancer l'API et le Frontend.
        
    - Explication des choix techniques et rappel des identifiants de test.