import os
from dotenv import load_dotenv

# Charge les variables depuis le fichier .env
load_dotenv()

# Clé secrète pour signer les tokens JWT
SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    raise ValueError("SECRET_KEY introuvable dans le fichier .env")

# Algorithme utilisé pour encoder/décoder les tokens JWT
ALGORITHM = os.getenv("ALGORITHM", "HS256")  # HS256 par défaut si absent du .env

# Durée de vie d'un token en heures
ACCESS_TOKEN_EXPIRE_HOURS = int(os.getenv("ACCESS_TOKEN_EXPIRE_HOURS", "24"))

# URL de connexion à la base de données
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL introuvable dans le fichier .env")