
# 🥔 ChipsUI

Bienvenue dans **ChipsUI**, l'interface ultime dédiée à la gestion et au suivi de votre collection de chips !

---

## 📋 Prérequis

* **[Docker Desktop](https://www.docker.com/products/docker-desktop/)** (version 4.29.0 ou supérieure) doit être installé et en cours d'exécution.

---

## 🚀 Configuration et lancement

1. Assurez-vous que **Docker Desktop** est bien démarré.
2. Ouvrez votre terminal à la racine du projet.
3. Lancez la commande suivante :

```bash
docker compose up
```

4. Une fois les services démarrés, cliquez sur les liens ci-dessous pour ouvrir les interfaces :
    

- 🌐 **Application Web (Frontend) :** [http://localhost:5173/](http://localhost:5173/)
    
- ⚙️ **API & Documentation (Swagger) :** [http://localhost:8000/docs](http://localhost:8000/docs)
    

## 🛠️ Commandes utiles

| **Action**                     | **Commande**             | **Description**                                                            |
| ------------------------------ | ------------------------ | -------------------------------------------------------------------------- |
| **Relancer les conteneurs**    | `docker compose start`   | Redémarre toute la stack après un redémarrage du PC sans tout réinstaller. |
| **Stopper l'application**      | `docker compose stop`    | Mettre en pause les conteneurs sans supprimer les données.                 |
| **Nettoyer la stack**          | `docker compose down`    | Arrête et supprime tous les conteneurs du projet proprement.               |
| **Purger les données (Reset)** | `docker compose down -v` | Supprime les conteneurs **et** réinitialise la base de données PostgreSQL. |
| **Voir les logs**              | `docker compose logs -f` | Affiche les logs en temps réel pour déboguer.                              |



> 💡 **Note :** Ce README permet de lancer l'intégralité de l'application via Docker. Les dossiers `/api` et `/web` contiennent la documentation spécifique à chaque brique si vous souhaitez contribuer au code ou travailler en développement local sans Docker.