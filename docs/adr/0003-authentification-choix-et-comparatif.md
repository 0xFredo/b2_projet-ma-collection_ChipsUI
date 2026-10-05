# ADR 0003 : Choix du protocole utilisé pour le jeton JWT

## Statut
Remplace [ADR 0001 : Authentification et autorisation via OAuth2](0001-Methode_OAuth2.md)

## Contexte
L'utilisation de jetons JWT (JSON Web Tokens) étant imposée par le sujet du TP pour authentifier les utilisateurs, il restait à déterminer quel protocole et quelle stratégie de transmission adopter entre le frontend React et l'API FastAPI.

## Options envisagées (toutes basées sur JWT)

### Option 1 : Authentification basique sur `/login` avec retour de JWT brut
* **Principe :** Un simple formulaire envoyant du JSON (`{"username": "...", "password": "..."}`) à un endpoint de connexion personnalisé qui renvoie directement le jeton JWT.
* **Avantages :** Implémentation rapide et très simple à prototyper.
* **Inconvénients :** Non standardisé, nécessite d'écrire des middlewares sur mesure pourSwagger UI et rend l'intégration des flux de sécurité moins interopérable.

### Option 2 : JWT transmis via Cookies `HttpOnly` / `SameSite`
* **Principe :** Le JWT est généré par l'API puis stocké directement dans un cookie sécurisé géré par le navigateur.
* **Avantages :** Protection optimale contre les attaques XSS (le code JavaScript client n'a pas accès au jeton).
* **Inconvénients :** Nécessite la gestion des protections CSRF et complexifie la configuration CORS entre des domaines/ports différents en environnement de développement.

### Option 3 : Standard OAuth2 avec flux `Password` (Option retenue)
* **Principe :** Utilisation du standard OAuth2 (`Resource Owner Password Credentials Grant`) via la route `POST /auth/login`, avec envoi du JWT dans l'en-tête HTTP `Authorization: Bearer <token>`.
* **Avantages :** Standard de l'industrie, intégration native et automatique dans FastAPI (`OAuth2PasswordBearer`) et Swagger UI pour les tests, parfait pour une API stateless découplée du frontend React.
* **Inconvénients :** Le stockage du jeton côté client (ex. `localStorage` ou état React) demande une vigilance contre les failles XSS.

## Décision
Nous avons retenu l'**Option 3 (OAuth2 Password Flow)**. Elle permet de respecter la contrainte du JWT tout en s'appuyant sur un standard reconnu et parfaitement supporté par l'écosystème FastAPI.

## Conséquences
- L'**ADR 0001** est marqué comme remplacé par le présent ADR.
- L'implémentation sur la route `POST /auth/login` et la validation du jeton via la dépendance `get_current_user` sont maintenues.