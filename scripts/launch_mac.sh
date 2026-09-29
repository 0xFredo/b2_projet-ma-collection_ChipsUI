echo "Lancement de ChipsUI..."

docker start postgres-chips
source venv/bin/activate
cd api
python -m uvicorn main:app --reload
cd ..

cd web
npm run dev