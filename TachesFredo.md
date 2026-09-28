## Plan : Frontend « Ma Collection »

Le frontend actuel est un squelette Vite : les types sont déjà présents, mais les pages, le client API, les contextes et les routes protégées restent à construire. Le contrat PDF sera la source de vérité, et le backend/zip servira à confirmer l’univers et les champs spécifiques.

**Étapes**

### 1. Recalage backend/frontend
1. Vérifier dans le zip et le backend :
   - URL `http://localhost:8000`
   - champs exacts de `Item`
   - catégories et données seedées
   - format réel des erreurs
2. Confirmer l’univers choisi et ses champs spécifiques.
3. Vérifier CORS, le démarrage du backend et `VITE_API_URL`.

### 2. Fondations techniques
4. Compléter `web/src/types/api.ts` avec les types de requêtes, filtres, erreurs et réponses.
5. Implémenter le hook générique `web/src/hooks/useLocalStorage.ts`.
6. Implémenter `web/src/services/api.ts` comme client HTTP unique :
   - `GET`, `POST`, `PATCH`, `DELETE`
   - ajout automatique du Bearer token
   - parsing des erreurs `{ erreur: { code, message } }`
   - fonctions pour toutes les routes FastAPI
7. Créer les composants partagés : layout, navigation, états de chargement/erreur/vide, cartes et formulaires.

### 3. Authentification et routes
8. Implémenter `web/src/context/AuthContext.tsx` :
   - token persistant
   - utilisateur courant
   - inscription, connexion, déconnexion
   - appel à `/auth/me`
   - invalidation si token expiré
9. Implémenter `web/src/components/ProtectedRoute.tsx`.
10. Modifier `web/src/main.tsx` pour monter `AuthProvider`.
11. Remplacer `web/src/routes.tsx` par :
   - `/`
   - `/items/:itemId`
   - `/login`
   - `/register`
   - `/collection`
   - `/stats`
12. Créer les pages `Login.tsx` et `Register.tsx` avec validation, chargement et erreurs API.

### 4. Catalogue public
13. Créer `Catalog.tsx` :
   - recherche avec debounce de 400 ms
   - filtre par catégorie
   - pagination
   - états chargement/erreur/vide
14. Créer `ItemCard`, `CatalogFilters` et `Pagination`.
15. Créer `ItemDetail.tsx` avec gestion du 404.
16. Ajouter le formulaire d’ajout à la collection :
   - statut
   - note de 1 à 5
   - commentaire
   - gestion du doublon 409

### 5. Collection et statistiques
17. Créer `CollectionContext.tsx` pour centraliser le chargement et les mutations.
18. Créer `Collection.tsx` avec :
   - filtre par statut
   - tri par date ou note
   - affichage de l’item imbriqué
19. Créer `CollectionEntryCard` et `CollectionEntryForm` :
   - modification avec `PATCH`
   - suppression avec `DELETE`
   - confirmation et messages d’erreur
20. Créer `Stats.tsx` :
   - total
   - répartition par statut
   - note moyenne

### 6. Design et finalisation
21. Remplacer les styles Vite de `web/src/styles.css` par une interface cohérente et responsive à 375 px.
22. Vérifier tous les états : chargement, erreur, vide, succès et mutation.
23. Tester les erreurs 401, 404, 409 et l’expiration du token.
24. Mettre à jour les README avec l’installation, `VITE_API_URL` et le lancement complet.
25. Effectuer le scénario final :

Inscription → connexion → catalogue → recherche → détail → ajout → modification → suppression → statistiques → déconnexion.

**Vérification**

Après chaque phase :

- `cd web && npm run build`
- `npm run lint`
- vérifier qu’il n’existe aucun `any`
- tester les routes avec et sans token
- tester l’affichage à 375 px
- vérifier les codes 201, 200, 204, 404 et 409

Les tests Vitest, le thème sombre et les autres bonus seront ajoutés seulement après la conformité fonctionnelle.
