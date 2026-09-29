echo Étape 1/7 (Python, environnement) — Initialisation...
python -m venv venv
call venv\Scripts\activate.bat



echo Étape 2/7 (Python, dépendances) — Installation en cours...
pip install -r api\requirements.txt



echo Étape 3/7 (Variables d'environnement) — Configuration...
cd api
python make_env.py
cd ..



echo Étape 4/7 (Docker) — Lancement du conteneur...
docker run --name postgres-chips -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=postgres -e POSTGRES_DB=chips_db -p 5432:5432 -d postgres



echo Étape 5/7 (Base de données) — Initialisation...
cd api
python -m db.seed
cd ..



echo Étape 6/7 (Nodejs, dépendances) — Installation en cours...
cd web
npm install
cd ..



echo Étape 7/7 () — 