# seed.py - Remplit la table english_words avec des mots de vocabulaire
# Pour lancer : .venv\Scripts\python.exe seed.py

import psycopg2
from config import DATABASE_URL

words = [
    # --- FACILE ---
    ("cat", "chat", "facile"),
    ("dog", "chien", "facile"),
    ("hello", "bonjour", "facile"),
    ("water", "eau", "facile"),
    ("house", "maison", "facile"),
    ("car", "voiture", "facile"),
    ("book", "livre", "facile"),
    ("sun", "soleil", "facile"),
    ("moon", "lune", "facile"),
    ("tree", "arbre", "facile"),
    ("fish", "poisson", "facile"),
    ("bird", "oiseau", "facile"),
    ("door", "porte", "facile"),
    ("chair", "chaise", "facile"),
    ("bread", "pain", "facile"),
    ("milk", "lait", "facile"),
    ("fire", "feu", "facile"),
    ("hand", "main", "facile"),
    ("eye", "oeil", "facile"),
    ("food", "nourriture", "facile"),

    # --- MOYEN ---
    ("library", "bibliothèque", "moyen"),
    ("weather", "météo", "moyen"),
    ("kitchen", "cuisine", "moyen"),
    ("hospital", "hôpital", "moyen"),
    ("mountain", "montagne", "moyen"),
    ("bridge", "pont", "moyen"),
    ("window", "fenêtre", "moyen"),
    ("garden", "jardin", "moyen"),
    ("butter", "beurre", "moyen"),
    ("forest", "forêt", "moyen"),
    ("market", "marché", "moyen"),
    ("mirror", "miroir", "moyen"),
    ("bottle", "bouteille", "moyen"),
    ("candle", "bougie", "moyen"),
    ("flower", "fleur", "moyen"),
    ("cheese", "fromage", "moyen"),
    ("pencil", "crayon", "moyen"),
    ("church", "église", "moyen"),
    ("farmer", "fermier", "moyen"),
    ("carpet", "tapis", "moyen"),

    # --- DIFFICILE ---
    ("butterfly", "papillon", "difficile"),
    ("squirrel", "écureuil", "difficile"),
    ("strawberry", "fraise", "difficile"),
    ("lighthouse", "phare", "difficile"),
    ("exhausted", "épuisé", "difficile"),
    ("ambiguous", "ambigu", "difficile"),
    ("threshold", "seuil", "difficile"),
    ("conscience", "conscience", "difficile"),
    ("sovereignty", "souveraineté", "difficile"),
    ("melancholy", "mélancolie", "difficile"),
    ("ephemeral", "éphémère", "difficile"),
    ("perseverance", "persévérance", "difficile"),
    ("eloquence", "éloquence", "difficile"),
    ("inevitable", "inévitable", "difficile"),
    ("inheritance", "héritage", "difficile"),
    ("acknowledge", "reconnaître", "difficile"),
    ("prosperous", "prospère", "difficile"),
    ("overwhelm", "submerger", "difficile"),
    ("bewildered", "déconcerté", "difficile"),
    ("magnificent", "magnifique", "difficile"),
]

connexion = psycopg2.connect(DATABASE_URL)
curseur = connexion.cursor()

# Vide la table avant d'insérer pour éviter les doublons
curseur.execute("DELETE FROM english_words")

curseur.executemany(
    "INSERT INTO english_words (english_traduction, french_traduction, level) VALUES (%s, %s, %s)",
    words
)

connexion.commit()

# Vérification
curseur.execute("SELECT COUNT(*) FROM english_words")
count = curseur.fetchone()[0]
connexion.close()

print(f"✓ {count} mots insérés dans la base de données.")
