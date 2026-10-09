# Guide utilisateur — ChipsUI

ChipsUI est une solution vous permettant de collectionner et organiser différents goûts et types de chips, avec une note et le statut de votre découverte pour chaque élément.

## Démarrage rapide

1. Vérifiez que Docker Desktop est bien installé et lancé.

2. Ouvrez un terminal à la racine de votre projet et exécutez la commande suivante :

        docker compose up

3. Puis ouvrez l'URL suivante dans votre navigateur : [http://localhost:5173/](http://localhost:5173/)

> Vous pouvez à présent créer un compte et commencer à construire votre collection.

## Fonctionnalités clés

### Création de compte

Pour créer votre compte et commencer à collectionner vos parfums préférés de chips, commencer par cliquer sur "S'inscrire" dans le coin supérieur droit de votre écran. Vous pouvez aussi vous connecter si vous avez déjà un compte.

![001](/docs/img/001.png)

Saisissez une adresse e-mail et un mot de passe d'au moins 6 caractères, puis finalisez la création du compte.

![002](/docs/img/002.png)

> Vous serez déjà connecté et redirigé à la page d'accueil.

### Ajout à la bibliothèque

Vous pouvez maintenant ajouter des chips à votre collection : de retour sur le catalogue, vous pouvez parcourir celui-ci, effectuer une recherche ou appliquer un filtre à l'aide des différentes options proposées en en-tête...

![003](/docs/img/003.png)

Une fois le parfum de votre choix sélectionnez, cliquez sur "Voir la fiche →" pour consulter les détails, ou "+ Ajouter à ma collection" pour directement l'ajouter à votre collection.

### Gestion de la bibliothèque

Cliquez sur l'onglet "Ma collection".

![004](/docs/img/004.png)

Pour chaque goût de chips enregistré, vous pouvez accéder à deux menus déroulants : la note, pour attribuer une note sur 5 à ce goût ; et le statut de découverte...

- "À découvrir" quand vous n'avez pas encore essayé...
- "En cours" quand vous êtes en train de tester...
- "Terminée" quand le découverte est finie...

### Consultation de vos statistiques

Rendez-vous dans l'onglet "Statistiques" : ici vous avez accès à une palette d'informations sur votre collection...

- Le nombre total d'éléments dans votre collection...
- La note moyenne attribuée sur tous les paquets...
- La répartition de l'état de découverte de vos goûts...

## Commandes utiles

| **Action**                    | **Commande**             | **Description**                                                           |
| ----------------------------- | ------------------------ | ------------------------------------------------------------------------- |
| **Relancer les conteneurs**   | `docker compose start`   | Redémarre l'application après un redémarrage du PC sans tout réinstaller. |
| **Stopper l'application**     | `docker compose stop`    | Mettre en pause l'application sans supprimer les données.                 |
| **Nettoyer les fichiers**     | `docker compose down`    | Arrête et supprime les fichiers du projet proprement.                     |
| **Purger toutes les données** | `docker compose down -v` | Supprime les fichiers **et** réinitialise la base de données.             |
| **Voir les logs**             | `docker compose logs -f` | Affiche les logs en temps réel pour une résolution de bugs.               |

## FAQ