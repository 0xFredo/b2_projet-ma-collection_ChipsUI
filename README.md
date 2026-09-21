Readme temporaire sur cette branche

Crée le .env dans api/ :

coller le contenu de .env.example dans le .env que vous avez crée dans le dossier api

Lancer le serveur:

uvicorn main:app --reload

Dépendances à installer:

pip install -r requirements.txt

Powershell:

admin: Set-ExecutionPolicy RemoteSigned -Scope CurrentUser

activer le venv:

python -m venv venv
.\venv\Scripts\Activate.ps1
pip freeze > requirements.txt
pip install -r requirements.txt


mac:

