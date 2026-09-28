# 📋 Todo-List Frontend (`web/`) — Application "Ma Collection"

## 1. ⚙️ Configuration & Architecture Générale

- [ ] **Initialisation du projet**
    
    - [ ] S'assurer que le projet est dans le dossier `web/` à la racine du dépôt Git.
        
    - [ ] Vérifier que `strict: true` est activé dans `tsconfig.json`.
        
    - [ ] Configurer la politique **"Zéro `any`"** (utiliser `unknown` avec vérification si nécessaire).
        
- [ ] **Système de styles (Sans librairie externe)**
    
    - [ ] Mettre en place le CSS (CSS classique, CSS Modules ou Tailwind).
        
    - [ ] S'assurer d'aucune dépendance à MUI, Chakra UI, Bootstrap, etc.
        
    - [ ] Définir les variables / thèmes réutilisables.
        
    - [ ] Valider que le design est **100 % Responsive** (lisible et utilisable dès 375 px de largeur).
        
- [ ] **Découpage & Règle des composants**
    
    - [ ] Utiliser exclusivement des **composants fonctionnels** avec props typées explicitement.
        
    - [ ] Vérifier qu'aucun composant ne dépasse **150 lignes de code**.
        
    - [ ] S'assurer que chaque boucle `.map()` utilise une `key` stable non basée sur l'index (`key={item.id}`).
        

## 2. 📐 Typage TypeScript (`src/types/`)

- [ ] **Fichier `src/types/api.ts`**
    
    - [ ] Écrire les types à la main (interdiction d'utiliser la génération automatique OpenAPI).
        
    - [ ] Définir l'union littérale de statut : `type Statut = "a_decouvrir" | "en_cours" | "termine";`
        
    - [ ] Définir l'interface `Item` (id, titre, categorie, description, image_url, annee + 1 ou 2 champs spécifiques à l'univers).
        
    - [ ] Définir l'interface `CollectionEntry` (id, statut, note [1-5], commentaire, date_ajout, item: Item).
        
    - [ ] Définir les interfaces de requêtes/réponses :
        
        - `RegisterPayload`, `LoginPayload`, `TokenResponse`
            
        - `PaginatedItemsResponse` (total, page, limit, results: Item[])
            
        - `AddToCollectionPayload`, `UpdateCollectionPayload`
            
        - `StatsResponse` (total, par_statut, note_moyenne)
            
        - `ApiError` (`{ erreur: { code: number, message: string } }`).
            

## 3. 🌐 Client HTTP Unique (`src/services/`)

- [ ] **Fichier `src/services/apiClient.ts`**
    
    - [ ] Centraliser **tous** les appels réseau `fetch` dans ce client unique (aucun `fetch`/`axios` direct dans les composants/pages).
        
    - [ ] Configurer l'URL de base (`http://localhost:8000`).
        
    - [ ] Intercepter le token JWT (depuis le stockage) et injecter automatiquement l'en-tête `Authorization: Bearer <token>` sur les requêtes authentifiées.
        
    - [ ] Gérer et traduire le format d'erreur maison de l'API (`{ erreur: { code, message } }`) en type/erreur TypeScript exploitable.
        
    - [ ] Implémenter les méthodes d'API :
        
        - **Auth** : `register()`, `login()`, `getMe()`
            
        - **Catalogue** : `getItems(q, categorie, page, limit)`, `getItemById(id)`
            
        - **Collection** : `getCollection(statut, tri)`, `addToCollection()`, `updateEntry()`, `deleteEntry()`
            
        - **Stats** : `getStats()`
            

## 4. 🪝 Hooks Personnalisés & Contexts (`src/hooks/` & `src/context/`)

- [ ] **Hook générique `useLocalStorage<T>`**
    
    - [ ] Implémenter la signature exacte : `function useLocalStorage<T>(cle: string, valeurInitiale: T): [T, (v: T) => void]`.
        
- [ ] **Hook `useDebounce<T>`**
    
    - [ ] Implémenter un hook de debounce (~400 ms) pour le champ de recherche du catalogue.
        
- [ ] **`AuthContext` (`src/context/AuthContext.tsx`)**
    
    - [ ] Stocker le token JWT et les informations de l'utilisateur courant (`GET /auth/me`).
        
    - [ ] Fournir les méthodes : `login`, `register`, `logout`.
        
    - [ ] Persister le token dans le `localStorage` via `useLocalStorage`.
        
- [ ] **`CollectionContext` (`src/context/CollectionContext.tsx`)**
    
    - [ ] Centraliser l'état global de la collection de l'utilisateur authentifié.
        
    - [ ] Fournir les fonctions de rechargement, d'ajout, de mise à jour et de suppression des éléments.
        

## 5. 🛣️ Routing & Protections (`src/router/`)

- [ ] Configuration de **React Router**
    
- [ ] **Composant `ProtectedRoute`**
    
    - [ ] Vérifier la présence d'un token valide dans `AuthContext`.
        
    - [ ] Rediriger automatiquement vers `/login` pour les pages protégées si non authentifié.
        
- [ ] **Déclarer la carte des routes :**
    
    - `/` ou `/catalogue` : Catalogue public
        
    - `/items/:id` : Fiche détaillée d'un élément
        
    - `/login` : Page de connexion
        
    - `/register` : Page d'inscription
        
    - `/collection` _(Protégée)_ : Collection personnelle
        
    - `/stats` _(Protégée)_ : Statistiques
        

## 6. 💻 Écrans & Composants UI (`src/pages/` & `src/components/`)

> ⚠️ **Règle absolue sur CHAQUE écran effectuant un appel API :** Traiter explicitement les 3 états : **Chargement** (Loader/Spinner), **Erreur** (Message explicite), et **Vide** (Empty state).

- [ ] **6.1 Page d'Authentification (`/login` & `/register`)**
    
    - [ ] Formulaire d'inscription : Email + Mot de passe.
        
    - [ ] Formulaire de connexion : Email + Mot de passe.
        
    - [ ] Gestion des erreurs d'authentification (ex: 409 email déjà pris, 401 identifiants invalides).
        
    - [ ] Redirection après connexion réussie.
        
- [ ] **6.2 Page Catalogue Public (`/` ou `/catalogue`)**
    
    - [ ] Champ de recherche par mot-clé `q` avec **debounce d'environ 400 ms**.
        
    - [ ] Barre de filtre par catégorie.
        
    - [ ] Pagination (contrôles `page` et `limit`).
        
    - [ ] Grille de cartes pour afficher les items.
        
    - [ ] Bouton / Action pour ouvrir la fiche détaillée ou ajouter à sa collection.
        
- [ ] **6.3 Fiche Détaillée (`/items/:id`)**
    
    - [ ] Affichage complet des informations de l'item (titre, image, catégorie, description, année, champs spécifiques).
        
    - [ ] Si l'utilisateur est connecté : bouton d'ajout à la collection (avec choix du statut, note et commentaire).
        
    - [ ] Bloquer/masquer l'ajout si l'élément est déjà dans la collection.
        
- [ ] **6.4 Page Collection Personnelle (`/collection`) — _Protégée_**
    
    - [ ] Filtre par statut (`a_decouvrir`, `en_cours`, `termine`).
        
    - [ ] Tri dynamique par date d'ajout ou par note.
        
    - [ ] Édition d'une entrée : modifier le statut, la note (1 à 5) et le commentaire.
        
    - [ ] Suppression d'une entrée de la collection.
        
- [ ] **6.5 Page Statistiques (`/stats`) — _Protégée_**
    
    - [ ] Affichage du nombre total d'entrées.
        
    - [ ] Répartition par statut (ex: X à découvrir, Y en cours, Z terminés).
        
    - [ ] Affichage de la note moyenne.
        

## 7. 🛡️ Contrôles Sécurité & Livrables

- [ ] **Vérification Sécurité & Soutenance**
    
    - [ ] Vérifier qu'aucun mot de passe ou secret n'est écrit ou loggué en clair côté front.
        
    - [ ] Préparer l'explication théorique du stockage JWT en `localStorage` vs `httpOnly cookies` pour la soutenance.
        
- [ ] **Livrables & Documentation Git**
    
    - [ ] Rédiger le fichier `web/README.md` expliquant la procédure d'installation et de lancement du frontend (`npm install`, `npm run dev`).
        
    - [ ] S'assurer que `node_modules/` et `.env` sont bien dans le `.gitignore`.
        
    - [ ] Effectuer des commits réguliers et explicites tout au long du développement (éviter le commit unique).