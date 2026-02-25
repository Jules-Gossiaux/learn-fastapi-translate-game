import sqlite3
import os

# Supprimer l'ancienne base pour repartir de zéro
if os.path.exists("exercice3.db"):
    os.remove("exercice3.db")
    print("🗑️  Ancienne base supprimée")

connexion = sqlite3.connect("exercice3.db")
cur = connexion.cursor()

cur.execute("""

""")

cur.execute("""
    CREATE TABLE IF NOT EXISTS joueurs(
        id INTEGER PRIMARY KEY,
        pseudo TEXT UNIQUE,
        niveau TEXT
    )
""")

cur.execute("""
    CREATE TABLE IF NOT EXISTS scores(
        id INTEGER PRIMARY KEY,
        joueur_id INTEGER,
        points INTEGER,
        date TEXT
    )
""")
connexion.commit()

joueurs = [
    ("Alice", "difficile"),
    ("Bob", "moyen"),
    ("Jules", "facile")
]

ids = []
for joueur in joueurs:
    cur.execute("INSERT INTO joueurs (pseudo, niveau) VALUES (?, ?)", (joueur[0], joueur[1]))
    ids.append(cur.lastrowid)

alice_id, bob_id, jules_id = ids

cur.execute("INSERT INTO scores (joueur_id, points, date) VALUES (?, 100, '2023-10-02')", (alice_id,))
cur.execute("INSERT INTO scores (joueur_id, points, date) VALUES (?, 40, '2023-10-04')", (bob_id,))
cur.execute("INSERT INTO scores (joueur_id, points, date) VALUES (?, 80, '2023-10-04')", (jules_id,))
connexion.commit()

cur.execute("""
    SELECT pseudo, points FROM joueurs
    INNER JOIN scores
        ON joueurs.id = scores.joueur_id
""")
rows = cur.fetchall()
for row in rows:
    print(row)
    
cur.execute("""
    SELECT pseudo, SUM(points) 
    FROM scores
    INNER JOIN joueurs
        ON scores.joueur_id = joueurs.id
    GROUP BY joueurs.pseudo
""")

print("total par joueur")
rows = cur.fetchall()
for row in rows:
    print(row)
    
cur.execute("""
    SELECT pseudo, MAX(points)
    FROM scores
    INNER JOIN joueurs
        ON scores.joueur_id = joueurs.id
""")
print(f"le meilleur score est: {cur.fetchall()}")
