# ChipsUI

Bienvenue dans ChipsUI, votre nouvelle inerface préférée dédiée à votre collection de chips.

> ***Prérequis :***
>
> - Docker Desktop 4.92.0 — [Télécharger](https://www.docker.com/products/docker-desktop/)

## Configuration et exécution

À la racine du projet exécutez la commande suivante :

    docker compose up

L'API et la documentation Swagger seront accessibles sur : `http://localhost:8000/docs`

## Commandes utiles

**Relancer le conteneur Docker après un redémarrage PC :**

``` PowerShell
docker start postgres-chips
```

**Supprimer le conteneur :**

``` PowerShell
docker rm -f postgres-chips
```