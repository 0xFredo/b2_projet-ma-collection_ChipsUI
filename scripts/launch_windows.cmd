echo "Lancement de ChipsUI..."

docker start postgres-chips
cd api
python -m uvicorn main:app --reload

npm run dev