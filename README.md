Readme temporaire sur cette branche

Lancer le serveur:

uvicorn main:app --reload

Dépendances à installer:

fastapi
uvicorn[standard]
sqlalchemy
pydantic

powershell:

admin: Set-ExecutionPolicy RemoteSigned -Scope CurrentUser

activer le venv:

python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt


mac:

