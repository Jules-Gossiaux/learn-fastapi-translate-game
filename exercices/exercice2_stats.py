import sqlite3
import os

# Supprimer l'ancienne base pour repartir de zéro
if os.path.exists("exercice2.db"):
    os.remove("exercice2.db")
    print("🗑️  Ancienne base supprimée")

connexion = sqlite3.connect("exercice2.db")
cur = connexion.cursor()

cur.execute("""
    CREATE TABLE IF NOT EXISTS parties(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        joueur TEXT,
        score INTEGER,
        duree_secondes INTEGER,
        date TEXT
    ) 
""")
connexion.commit()

cur.execute("""
    INSERT INTO parties
    (joueur, score, duree_secondes, date)
    VALUES
    ("Alice", 150, 120, "2023-10-01"),
    ("Alice", 200, 95, "2023-10-01"),
    ("Charlie", 180, 110, "2023-10-02"),
    ("Hugo", 50, 300, "2023-10-02"),
    ("Emma", 220, 90, "2023-10-03"),
    ("Bob", 120, 140, "2023-10-03"),
    ("Emma", 300, 60, "2023-10-04"),
    ("Hugo", 90, 200, "2023-10-04"),
    ("Bob", 175, 115, "2023-10-05"),
    ("Hugo", 210, 100, "2023-10-05")
""")
connexion.commit()
print(cur.fetchall())
cur.execute("SELECT AVG(score) FROM parties")
print(f"Average: {cur.fetchall}")


cur.execute("""
    SELECT joueur, COUNT(score) FROM parties GROUP BY joueur            
""")
print(cur.fetchall())

cur.execute("SELECT * FROM PARTIES ORDER BY score DESC LIMIT 3")
print(cur.fetchall())


cur.execute("""
    SELECT SUM(score) FROM parties WHERE joueur = "Alice"
""")
print(cur.fetchall())

cur.execute("SELECT * FROM parties WHERE score > 100")
print(cur.fetchall())