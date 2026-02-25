import sqlite3
from passlib.context import CryptContext
from datetime import datetime

DB_FILE = "users.db"

# Configuration pour le hashing des mots de passe
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

# ============================================
# FONCTION 1 : Connexion
# ============================================
def get_connexion():
    connexion = sqlite3.connect(DB_FILE)
    connexion.execute("PRAGMA foreign_keys = ON")
    return connexion

# ============================================
# FONCTION 2 : Initialiser la DB
# ============================================
def init_db():
    # Créer la table users (id, username UNIQUE, hashed_password, created_at)
    connexion = get_connexion()
    curseur = connexion.cursor()
    
    curseur.execute("""
                    CREATE TABLE if NOT exists users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT UNIQUE NOT NULL,
                        hashed_password TEXT NOT NULL,
                        created_at TEXT
                    )    
                """)
    connexion.commit()
    connexion.close()
# ============================================
# FONCTION 3 : Créer un utilisateur
# ============================================
def create_user(username, password):
    # Hasher le password avec pwd_context.hash(password)
    # Insérer dans users
    # Retourner l'ID créé
    connexion = get_connexion()
    curseur = connexion.cursor()
    
    hashed_password = pwd_context.hash(password)
    
    curseur.execute("INSERT INTO users (username, hashed_password, created_at) VALUES (?, ?, ?)", (username, hashed_password, datetime.now().isoformat()))
    user_id = curseur.lastrowid
    connexion.commit()
    connexion.close()
    return user_id

# ============================================
# FONCTION 4 : Récupérer un user par username
# ============================================
def get_user_by_username(username):
    connexion = get_connexion()
    curseur = connexion.cursor()
    
    curseur.execute("SELECT * FROM users WHERE username = ?", (username,))
    user_tuple = curseur.fetchone()
    connexion.close()
    if user_tuple:
        user = {
            "id": user_tuple[0],
            "username": user_tuple[1],
            "hashed_password": user_tuple[2],
            "created_at": user_tuple[3]
        }
        return user
    else:
        return None

    


# ============================================
# FONCTION 5 : Vérifier le mot de passe
# ============================================
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)
# Initialiser la DB au chargement
init_db()
