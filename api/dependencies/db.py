# Dépendance d'injection de session BDD

from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession
from db.database import AsyncSessionLocal

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Dépendance FastAPI : ouvre une session, la yield pour la route, 
    puis la ferme proprement à la fin.
    """
    async with AsyncSessionLocal() as session:
        yield session


get_session = get_db
