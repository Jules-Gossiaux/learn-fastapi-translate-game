# database.py - Gestion de la base de données PostgreSQL
from passlib.context import CryptContext
import psycopg2
import psycopg2.extras

from config import DATABASE_URL

pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")


# ============================================
# FONCTION 1 : Connexion à la base de données
# ============================================

def get_connexion():
    """
    Crée et retourne une connexion à la base de données
    
    À toi de coder :
    1. Créer une connexion avec sqlite3.connect(DB_FILE)
    2. Activer les Foreign Keys avec : connexion.execute("PRAGMA foreign_keys = ON")
    3. Retourner la connexion
    
    Returns:
        sqlite3.Connection: La connexion à la base de données
    """
    # TON CODE ICI
    connexion = psycopg2.connect(DATABASE_URL)
    return connexion


# ============================================
# FONCTION 2 : Initialiser la base de données
# ============================================

def init_db():
    """
    Initialise la base de données avec les tables nécessaires
    
    À toi de coder :
    
    1. Créer la table "user" avec :
       - id (INTEGER PRIMARY KEY AUTOINCREMENT)
       - username (TEXT UNIQUE NOT NULL)
       - score (INTEGER DEFAULT 0)
       - attempts (INTEGER DEFAULT 0)
       - level (TEXT DEFAULT 'facile')
    
    2. Créer la table "historique" avec :
       - id (INTEGER PRIMARY KEY AUTOINCREMENT)
       - user_id (INTEGER NOT NULL)
       - mot (TEXT NOT NULL)
       - proposition (TEXT NOT NULL)
       - correct (INTEGER NOT NULL)  -- 1 pour vrai, 0 pour faux
       - bonne_reponse (TEXT NOT NULL)
       - date (TEXT NOT NULL)
       - FOREIGN KEY (user_id) REFERENCES user(id) ON DELETE CASCADE
    
    3. Vérifier si la table user est vide avec :
       SELECT COUNT(*) FROM user
    
    4. Si elle est vide, ajouter un user par défaut :
       username='user1', score=0, attempts=0, level='facile'
    
    5. N'oublie pas commit() et close() !
    
    Indice : Utilise CREATE TABLE IF NOT EXISTS pour éviter les erreurs
    """
    # TON CODE ICI
    connexion = get_connexion()
    curseur = connexion.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    curseur.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        score INTEGER DEFAULT 0,
        attempts INTEGER DEFAULT 0,
        level TEXT DEFAULT 'facile'
        )
        """
    )
    curseur.execute(
        """
        CREATE TABLE IF NOT EXISTS guesses (
        id SERIAL PRIMARY KEY,
        user_id INTEGER NOT NULL,
        word_id INTEGER NOT NULL,
        guess TEXT NOT NULL,
        is_correct INTEGER NOT NULL,
        date TEXT NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        )
        """
    )

    curseur.execute(
        """
        CREATE TABLE IF NOT EXISTS english_words (
            id SERIAL PRIMARY KEY,
            english_traduction TEXT NOT NULL,
            french_traduction TEXT NOT NULL,
            level TEXT NOT NULL
        )
        """
    )

    connexion.commit()
    connexion.close()



# ============================================
# FONCTION 5 : Mettre à jour le level
# ============================================

def change_level(user_id, new_level):
    connexion = get_connexion()
    curseur = connexion.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    
    curseur.execute("UPDATE users SET level=(%s) WHERE id=(%s)", (new_level, user_id))
    connexion.commit()
    connexion.close()

# ============================================
# FONCTION 6 : Ajouter une tentative à l'historique
# ============================================


# ============================================
# FONCTION 7 : Récupérer l'historique
# ============================================


# ============================================
# FONCTION 8 : Réinitialiser le user
# ============================================

def reset_user(user_id):
    """
    Réinitialise le score et les attempts du user à zéro
    et supprime tout son historique
    
    Args:
        user_id (int): L'ID du user à réinitialiser
    """
    connexion = get_connexion()
    curseur = connexion.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    
    curseur.execute("UPDATE users SET score = 0, attempts = 0 WHERE id = (%s)", (user_id,))
    curseur.execute("DELETE FROM guesses WHERE user_id = (%s)", (user_id,))
    connexion.commit()
    connexion.close()
    
    
def create_user(username, password, level="facile"):
    hashed_password = pwd_context.hash(password)
    
    connexion = get_connexion()
    curseur = connexion.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    
    curseur.execute("INSERT INTO users (username, password, level) VALUES ((%s), (%s), (%s)) RETURNING id", (username, hashed_password, level))
    user_id = curseur.fetchone()["id"]
    
    connexion.commit()
    connexion.close()
    
    return user_id


def get_user_by_username(username):
    connexion = get_connexion()
    curseur = connexion.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    curseur.execute("SELECT * FROM users WHERE username=(%s)", (username,))
    row = curseur.fetchone()
    connexion.close()
    if row:
        return dict(row)  # ✅ sqlite3.Row → dict, toutes les colonnes automatiquement
    return None

def verify_password(plain_password, hashed_password):
    return (pwd_context.verify(plain_password, hashed_password))



def get_random_word(language, level):
    connexion = get_connexion()
    curseur = connexion.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    if language == "english":
        curseur.execute("SELECT * FROM english_words WHERE level=(%s) ORDER BY RANDOM() LIMIT 1", (level,))
        row = curseur.fetchone()
        connexion.close()
        if row:
            return {
                "id": row["id"],
                "english_traduction": row["english_traduction"],
                "french_traduction": row["french_traduction"],
                "level": row["level"]
            }
        else:
            return None
    else:
        connexion.close()
        return None
        
        
def add_attemp(user_id, word_id, guess, is_correct, date):
    connexion = get_connexion()
    curseur = connexion.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    curseur.execute("""
                    INSERT INTO guesses
                    (user_id, word_id, guess, is_correct, date)
                    VALUES ((%s), (%s), (%s), (%s), (%s))
                """, (user_id, word_id, guess, is_correct, date))
    curseur.execute("UPDATE users SET attempts = attempts + 1 WHERE id = (%s)", (user_id,))
    if is_correct:
        curseur.execute("UPDATE users SET score = score + 1 WHERE id = (%s)", (user_id,))
    connexion.commit()
    connexion.close()
    
def get_guesses(user_id, limit=5):
    connexion = get_connexion()
    curseur = connexion.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    
    curseur.execute(
        """
            SELECT ew.english_traduction, ew.french_traduction, g.guess, g.date
            FROM guesses g
            JOIN english_words ew ON g.word_id = ew.id
            WHERE g.user_id = (%s) 
            ORDER BY g.date DESC
            LIMIT (%s)
        """, (user_id, limit)
    )
    rows = curseur.fetchall()
    guesses = []
    for row in rows:
        row_dict = {
                "english_traduction": row["english_traduction"],
                "french_traduction": row["french_traduction"],
                "guess": row["guess"],
                "date": row["date"]
            }
        guesses.append(row_dict)
    connexion.close()
    return guesses


def leaderboard(level):
    """
    Récupère le top 10 des utilisateurs par score

    Returns:
        list: Liste des dictionnaires contenant username, score et attempts
    """
    connexion = get_connexion()
    curseur = connexion.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    
    if level is None or level == "tous":
        curseur.execute("""
            SELECT username, score, attempts FROM users
            ORDER BY score DESC
            LIMIT 10
        """)
    else:
        curseur.execute("""
            SELECT username, score, attempts FROM users
            WHERE level = (%s)
            ORDER BY score DESC
            LIMIT 10
        """, (level,))
    
    rows = curseur.fetchall()
    connexion.close()
    return [dict(row) for row in rows]


def get_statistics(user_id):
    """
    Récupère les statistiques globales d'un utilisateur (total tentatives + correctes)

    Returns:
        dict: {total, correct}
    """
    connexion = get_connexion()
    curseur = connexion.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    
    curseur.execute("SELECT COUNT(*) as total, COALESCE(SUM(is_correct), 0) as correct FROM guesses WHERE user_id = (%s)", (user_id,))
    row = curseur.fetchone()
    connexion.close()
    return {
        "total": row["total"],
        "correct": row["correct"]
    }
    
def statistics_table(user_id):
    """
    Récupère les statistiques par niveau d'un utilisateur

    Returns:
        list: [{level, total, correct}, ...]
    """
    connexion = get_connexion()
    curseur = connexion.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    
    curseur.execute(
        """
            SELECT ew.level, COUNT(*) as total, SUM(g.is_correct) as correct 
            FROM guesses g
            JOIN english_words ew ON ew.id = g.word_id
            WHERE g.user_id = (%s)
            GROUP BY ew.level
            ORDER BY ew.level
        """, (user_id,)
    )
    rows = curseur.fetchall()
    connexion.close()
    return [dict(row) for row in rows]
# ============================================
# INITIALISATION AU CHARGEMENT DU MODULE
# ============================================

# Cette ligne appelle init_db() automatiquement quand on importe le module
init_db()
