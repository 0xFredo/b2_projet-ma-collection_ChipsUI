# Connexion aiosqlite / SQLAlchemy async

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlmodel import SQLModel
from core.config import settings

# Utilisation de l'URL définie dans config.py (qui lit le .env)
engine = create_async_engine(
    settings.DATABASE_URL, 
    echo=True, 
    future=True,
    connect_args={"check_same_thread": False}  # Obligatoire pour SQLite en async
)

# Fabrique de sessions asynchrones
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
    class_=AsyncSession,
)

async def init_db():
    """Crée les tables dans la base de données au démarrage."""
    # On importe les modèles ici pour que SQLModel enregistre les tables
    import models.user
    import models.item
    import models.collection

    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)