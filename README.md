# Readme temporaire (Branche Backend)

Suivre les étapes dans l'ordre pour lancer l'API en local.

---

### 1. Activer l'environnement virtuel et installer les dépendances

**Sous PowerShell (Windows) :**
> Si c'est la première fois, autoriser l'exécution des scripts :
> `Set-ExecutionPolicy RemoteSigned -Scope CurrentUser`

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### 2. Configurer les variables d'environnement

1. Crée un fichier `.env` dans le dossier `api/`.
    
2. Copie le contenu de `api/.env.example` dans ton `.env`.
    
3. Renseigne une clé secrète dans le champ `SECRET_KEY`.
    
### 3. Initialiser la base de données et lancer le serveur

``` PowerShell
# Se placer dans le dossier de l'API
cd api

# Générer la BDD et insérer les données de test
python -m db.seed

# Lancer le serveur avec rechargement automatique
python -m uvicorn main:app --reload
```

L'API et la documentation Swagger seront accessibles sur : `http://localhost:8000/docs`

### 📌 Rappel si ajout de nouvelles dépendances

Toujours exécuter la commande à la **racine du projet** :

``` PowerShell
pip freeze > requirements.txt
```