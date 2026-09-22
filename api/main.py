from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import models.user
import models.item
import models.collection

from routers import auth, items, collection

app = FastAPI(
    title="API Projet Collaborative",
    description="Documentation des endpoints",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(items.router)
app.include_router(collection.router)

@app.get("/")
def read_root():
    return {"message": "API en ligne"}