import sqlite3
import os

# Supprimer l'ancienne base pour repartir de zéro
if os.path.exists("exercice1.db"):
    os.remove("exercice1.db")
    print("🗑️  Ancienne base supprimée")

connexion = sqlite3.connect("exercice1.db")
curseur = connexion.cursor()

curseur.execute("""
    CREATE TABLE IF NOT EXISTS scores (
        id INTEGER PRIMARY KEY,
        joueur TEXT,
        points INTEGER,
        niveau TEXT
    )                
""")
connexion.commit()
curseur.execute("""
    INSERT INTO scores
    (joueur, points, niveau)
    VALUES ("Alice", 50, "difficile"), ("Antoine", 100, "difficile"), ("Jules", 80, "moyen"), ("Martin", 100, "difficile"), ("Emma", 20, "facile")                
""")
connexion.commit()
curseur.execute("""
    SELECT * FROM scores
    ORDER BY points DESC
""")
connexion.commit()
rows = curseur.fetchall()
for row in rows:
    print(row)
    
curseur.execute("""
    SELECT MAX(points)
    FROM scores
""")
connexion.commit()
print(f"Meilleur score: {curseur.fetchall()}")

curseur.execute("""
    UPDATE scores
    SET points = 90
    WHERE joueur = "Alice"
""")
connexion.commit()
print(f"points de alice augmenté: {curseur.fetchall()}")

curseur.execute("""
       DELETE FROM scores
       WHERE niveau = "facile"         
""")
connexion.commit()
print("Joueurs du niveau 'facile' supprimé")

curseur.execute("""
    SELECT * FROM scores
""")
connexion.commit()
rows = curseur.fetchall()
for row in rows:
    print(row)
    
connexion.close()