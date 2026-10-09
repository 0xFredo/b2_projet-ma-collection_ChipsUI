# Guide utilisateur — ChipsUI

ChipsUI est une solution vous permettant de collectionner et organiser différents goûts et types de chips, avec une note et le statut de votre découverte pour chaque élément.

## Démarrage rapide

1. Vérifiez que Docker Desktop est bien installé et lancé.

2. Ouvrez un terminal à la racine de votre projet et exécutez la commande suivante :

        docker compose up

3. Puis ouvrez l'URL suivante dans votre navigateur : [http://localhost:5173/](http://localhost:5173/)

> Vous pouvez à présent créer un compte et commencer à construire votre collection !

## Fonctionnalités clés

### Création de compte

### Ajout à la bibliothèque

## Commandes utiles

| **Action**                    | **Commande**             | **Description**                                                           |
| ----------------------------- | ------------------------ | ------------------------------------------------------------------------- |
| **Relancer les conteneurs**   | `docker compose start`   | Redémarre l'application après un redémarrage du PC sans tout réinstaller. |
| **Stopper l'application**     | `docker compose stop`    | Mettre en pause l'application sans supprimer les données.                 |
| **Nettoyer les fichiers**     | `docker compose down`    | Arrête et supprime les fichiers du projet proprement.                     |
| **Purger toutes les données** | `docker compose down -v` | Supprime les fichiers **et** réinitialise la base de données.             |
| **Voir les logs**             | `docker compose logs -f` | Affiche les logs en temps réel pour une résolution de bugs.               |