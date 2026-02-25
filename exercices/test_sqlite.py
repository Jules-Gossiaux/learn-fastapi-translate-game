# test_sqlite.py - Apprendre SQLite pas à pas

import sqlite3

# ============================================
# ÉTAPE 1 : Créer une connexion à la base de données
# ============================================

# Crée le fichier test.db s'il n'existe pas
connexion = sqlite3.connect("test.db")

# Un "curseur" pour exécuter des commandes SQL
curseur = connexion.cursor()

print("✓ Connexion établie avec la base de données !")

# ============================================
# ÉTAPE 2 : Créer une table
# ============================================

# SQL pour créer une table "joueurs"
# INTEGER = nombre entier
# TEXT = texte
# PRIMARY KEY = identifiant unique (se crée automatiquement)
curseur.execute("""
    CREATE TABLE IF NOT EXISTS joueurs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        pseudo TEXT NOT NULL,
        score INTEGER DEFAULT 0,
        tentatives INTEGER DEFAULT 0
    )
""")

print("✓ Table 'joueurs' créée !")

# ============================================
# ÉTAPE 3 : Ajouter des données (INSERT)
# ============================================

# Ajouter un joueur
curseur.execute("""
    INSERT INTO joueurs (pseudo, score, tentatives)
    VALUES ('Alice', 15, 30)
""")

# Ajouter un autre joueur
curseur.execute("""
    INSERT INTO joueurs (pseudo, score, tentatives)
    VALUES ('Bob', 8, 20)
""")

# IMPORTANT : Sauvegarder les changements
connexion.commit()

print("✓ Deux joueurs ajoutés !")

# ============================================
# ÉTAPE 4 : Lire des données (SELECT)
# ============================================

# Lire TOUS les joueurs
curseur.execute("SELECT * FROM joueurs")
tous_les_joueurs = curseur.fetchall()

print("\n📋 Tous les joueurs :")
for joueur in tous_les_joueurs:
    print(f"  ID: {joueur[0]}, Pseudo: {joueur[1]}, Score: {joueur[2]}, Tentatives: {joueur[3]}")

# Lire UN joueur spécifique
curseur.execute("SELECT * FROM joueurs WHERE pseudo = 'Alice'")
alice = curseur.fetchone()

print(f"\n👤 Alice : Score = {alice[2]}, Tentatives = {alice[3]}")

# ============================================
# ÉTAPE 5 : Modifier des données (UPDATE)
# ============================================

# Alice a gagné des points !
curseur.execute("""
    UPDATE joueurs
    SET score = score + 5
    WHERE pseudo = 'Alice'
""")
connexion.commit()

print("\n✓ Score d'Alice mis à jour !")

# Vérifier
curseur.execute("SELECT score FROM joueurs WHERE pseudo = 'Alice'")
nouveau_score = curseur.fetchone()[0]
print(f"  Nouveau score d'Alice : {nouveau_score}")

# ============================================
# ÉTAPE 6 : Supprimer des données (DELETE)
# ============================================

curseur.execute("DELETE FROM joueurs WHERE pseudo = 'Bob'")
connexion.commit()

print("\n✓ Bob supprimé de la base de données")

# ============================================
# ÉTAPE 7 : Fermer la connexion
# ============================================

connexion.close()
print("\n✓ Connexion fermée")

print("\n" + "="*50)
print("🎉 Test terminé !")
print("Un fichier 'test.db' a été créé dans ton dossier.")
print("Tu peux l'ouvrir avec DB Browser for SQLite pour le visualiser.")
print("="*50)
