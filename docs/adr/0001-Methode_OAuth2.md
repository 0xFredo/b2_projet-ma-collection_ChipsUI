# ADR 0001 : Authentification et autorisation via OAuth2 (Password Flow) et JWT

## Statut

Accepté

## Contexte

L'application nécessite un système d'authentification et d'autorisation sécurisé pour identifier les utilisateurs et protéger les routes sensibles de l'API (comme la gestion de la collection personnelle). Bien que la consigne initiale n'imposait pas de mécanisme particulier, il était indispensable de retenir une solution standard, évolutive et facile à intégrer côté frontend (React) et backend (FastAPI).

## Décision

Nous avons décidé d'implémenter le standard **OAuth2** en utilisant le flux `Resource Owner Password Credentials Grant` (OAuth2 Password Flow) couplé à des jetons **JWT (JSON Web Tokens)** signés avec un algorithme symétrique (HMAC-SHA256).

Concrètement :

- L'utilisateur s'authentifie via la route `/auth/login` en fournissant ses identifiants.
- L'API valide le mot de passe (haché via `bcrypt`) et génère un jeton JWT contenant l'identité de l'utilisateur (`sub`) et une durée d'expiration (`exp`).
- Le client (frontend React) stocke ce jeton et le transmet dans l'en-tête HTTP `Authorization: Bearer <token>` pour accéder aux routes protégées.
- FastAPI valide de manière asynchrone le jeton via une dépendance réutilisable (`get_current_user`).

## Conséquences

### Positives

- **Standard de l'industrie :** Compatibilité native avec FastAPI (`OAuth2PasswordBearer`, `OAuth2PasswordRequestForm`) et intégration directe avec l'interface Swagger UI pour tester les routes directement.
- **Stateless (sans état) :** Le serveur n'a pas besoin de stocker les sessions en base de données ou en mémoire Redis ; le jeton JWT contient toutes les informations nécessaires à l'authentification.
- **Sécurité renforcée :** Utilisation de hachage de mot de passe fort (`bcrypt`) et expiration automatique des jetons d'accès.

### Négatives / Compromis

- **Invalidation complexe :** Comme les jetons JWT sont stateless, il est difficile de révoquer un jeton spécifique avant son expiration sans maintenir une liste noire (_blacklist_) côté serveur.
- **Stockage client :** Nécessite une attention particulière côté frontend pour le stockage du jeton (éviter les failles XSS/CSRF).
