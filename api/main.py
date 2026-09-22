from fastapi import FastAPI

# Charger tous les modèles en mémoire pour résoudre les relations SQLAlchemy
import models.user
import models.item
import models.collection

from routers import auth

app = FastAPI(
    title="API Projet Collaborative",
    description="Documentation des endpoints",
    version="1.0.0"
)

# Liaison du routeur au serveur
app.include_router(auth.router)

@app.get("/")
def read_root():
    return {"message": "API en ligne"}