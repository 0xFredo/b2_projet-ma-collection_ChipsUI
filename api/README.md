# Readme Backend

Suivre les étapes dans l'ordre pour lancer l'API en local depuis la racine du projet.

---

### 1. Activer l'environnement virtuel et installer les dépendances

**Sous PowerShell (Windows) :**
> Si c'est la première fois, autoriser l'exécution des scripts :
> `Set-ExecutionPolicy RemoteSigned -Scope CurrentUser`

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r api/requirements.txt
```

### 2. Configurer les variables d'environnement

1. Crée un fichier `.env` dans le dossier `api/`.

2. Copie le contenu de `api/.env.example` dans ton `.env`.

3. Renseigne une clé secrète dans le champ `SECRET_KEY`.

OU executer depuis le dossier api/ : 
```
cd api
python -m make_env
```

### 3. Lancer la base de données PostgreSQL (Docker)

> Assure-toi que **Docker Desktop** est installé et démarré sur ta machine.
[Télécharger Docker Desktop](https://www.docker.com/products/docker-desktop/)

Ouvre un terminal et lance le conteneur PostgreSQL :

``` PowerShell
docker run --name postgres-chips -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=postgres -e POSTGRES_DB=chips_db -p 5432:5432 -d postgres
```

### 4. Initialiser la base de données et lancer le serveur



``` PowerShell
# Se placer dans le dossier de l'API
cd api

# Générer les tables PostgreSQL et insérer les données de test
python -m db.seed

# Lancer le serveur avec rechargement automatique
python -m uvicorn main:app --reload
```

L'API et la documentation Swagger seront accessibles sur : `http://localhost:8000/docs`

### 📌 Commandes utiles

**Relancer le conteneur Docker après un redémarrage PC :**

``` PowerShell
docker start postgres-chips
```

**Supprimer le conteneur :**

``` PowerShell
docker rm -f postgres-chips
```

**Mise à jour des dépendances (à exécuter à la racine du projet) :**

``` PowerShell
pip freeze > api/requirements.txt
```