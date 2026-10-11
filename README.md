
# ChipsUI

Bienvenue dans **ChipsUI**, l'interface ultime dédiée à la gestion et au suivi de votre collection de chips !

## Prérequis

* **[Docker Desktop](https://www.docker.com/products/docker-desktop/)** (version 4.29.0 ou supérieure) doit être installé et en cours d'exécution.

## Configuration et lancement

1. Assurez-vous que **Docker Desktop** est bien démarré.
2. Ouvrez votre terminal à la racine du projet.
3. Lancez la commande suivante :

        docker compose up

4. Une fois les services démarrés, cliquez sur les liens ci-dessous pour ouvrir les interfaces :

- **Application Web (Frontend) :** [http://localhost:5173/](http://localhost:5173/)
    
- **API & Documentation (Swagger) :** [http://localhost:8000/docs](http://localhost:8000/docs)

> **Note :** Ce README permet de lancer l'intégralité de l'application via Docker. Les dossiers `/api` et `/web` contiennent la documentation spécifique à chaque brique si vous souhaitez contribuer au code ou travailler en développement local sans Docker.

## Structure du projet

```text
.
├── docker-compose.yml        # Lance l'API et l'application web
├── README.md
│
├── docs/                     # DOCUEMTATION FONCTIONNELLE ET DÉCISIONS D'ARCHITECTURE
│   ├── user-guide.md         # GUIDE UTILISATEUR
│   └── adr/                  # Architecture Decision Records
│
├── api/                      # BACKEND FASTAPI (gestion API : utilisateurs, authentification, collections et items)
│   ├── main.py               # Point d'entrée de l'API
│   ├── core/                 # Configuration et sécurité
│   ├── db/                   # Connexion et initialisation de la base
│   ├── dependencies/         # Dépendances FastAPI partagées
│   ├── models/               # Modèles de données
│   ├── schemas/              # Schémas de validation des échanges API
│   └── routers/              # Routes HTTP (authentification, collection, items)
│
└── web/                      # Frontend REACT + TYPESCRIPT + VITE (interface de consultation et de gestion de la collection)
        ├── src/
        │   ├── components/       # Composants réutilisables et layout
        │   ├── context/          # États partagés (authentification, collection)
        │   ├── hooks/            # Hooks React personnalisés
        │   ├── pages/            # Écrans de l'application
        │   ├── services/         # Communication avec l'API
        │   ├── types/            # Types TypeScript
        │   ├── routes.tsx        # Définition des routes frontend
        │   └── main.tsx          # Point d'entrée React
        ├── package.json
        └── vite.config.ts
```