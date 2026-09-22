from fastapi import FastAPI
from routers import auth  # Import de ton routeur

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