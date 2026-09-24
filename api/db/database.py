# Connexion PostgreSQL / SQLAlchemy async

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlmodel import SQLModel
from core.config import settings

# Configuration du moteur pour PostgreSQL (sans connect_args SQLite)
engine = create_async_engine(
    settings.DATABASE_URL, 
    echo=True, 
    future=True
)

# Fabrique de sessions asynchrones
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
    class_=AsyncSession,
)

async def init_db():
    """Crée les tables dans PostgreSQL au démarrage."""
    # On importe les modèles pour que SQLModel enregistre les tables
    import models.user
    import models.item
    import models.collection

    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)