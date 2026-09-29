# ChipsUI

Bienvenue dans ChipsUI, votre nouvelle inerface préférée dédiée à votre collection de chips.

> ***Prérequis :***
>
> - Docker Desktop 4.92.0 — [Télécharger](https://www.docker.com/products/docker-desktop/)

## Configuration et exécution

### 1. Configurer les variables d'environnement

1. Crée un fichier `.env` dans le dossier `api/`.

2. Copie le contenu de `api/.env.example` dans ton `.env`.

3. Renseigne une clé secrète dans le champ `SECRET_KEY`.

OU executer depuis le dossier api/ : 

    cd api
    python -m make_env

### 2. Lancer la base de données PostgreSQL (Docker)

> Assure-toi que **Docker Desktop** est installé et démarré sur ta machine.
[Télécharger Docker Desktop](https://www.docker.com/products/docker-desktop/)

Ouvre un terminal et lance le conteneur PostgreSQL :

    docker run --name postgres-chips -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=postgres -e POSTGRES_DB=chips_db -p 5432:5432 -d postgres

### 4. Initialiser la base de données et lancer le serveur

    docker compose up

L'API et la documentation Swagger seront accessibles sur : `http://localhost:8000/docs`

### Commandes utiles

**Relancer le conteneur Docker après un redémarrage PC :**

``` PowerShell
docker start postgres-chips
```

**Supprimer le conteneur :**

``` PowerShell
docker rm -f postgres-chips
```