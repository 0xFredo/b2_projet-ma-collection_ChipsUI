import secrets
from pathlib import Path

env_path = Path(".env")

# Évite d'écraser un .env existant par accident
if env_path.exists():
    print(".env existe déjà. Opération annulée.")
    exit(0)

env_content = f"""DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/chips_db
SECRET_KEY={secrets.token_hex(32)}
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
"""

env_path.write_text(env_content)
print("Fichier .env généré avec succès !")