from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

import models.user
import models.item
import models.collection

from routers import auth, items, collection

app = FastAPI(
    title="API Projet Collaborative",
    description="Documentation de l'API REST 'Ma Collection'",
    version="1.0.0"
)

# CORS restreint au serveur de dev React Vite
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Exception Handler personnalisé pour respecter le format d'erreur imposé
@app.exception_handler(HTTPException)
async def custom_http_exception_handler(request: Request, exc: HTTPException):
    # Si le detail est déjà un dictionnaire contenant "erreur", on le renvoie tel quel
    if isinstance(exc.detail, dict) and "erreur" in exc.detail:
        return JSONResponse(status_code=exc.status_code, content=exc.detail)

    # Sinon on formate l'erreur au format exigé par le contrat : {"erreur": {"code": ..., "message": ...}}
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "erreur": {
                "code": exc.status_code,
                "message": str(exc.detail)
            }
        }
    )


app.include_router(auth.router)
app.include_router(items.router)
app.include_router(collection.router)


@app.get("/", include_in_schema=False)
def read_root():
    return {"message": "API Ma Collection en ligne"}