# test_database.py - Script pour tester database.py
import database
import os

# Supprimer l'ancienne base pour repartir de zéro
if os.path.exists("game.db"):
    os.remove("game.db")
    print("✓ Ancienne base supprimée")

# Réinitialiser la base
database.init_db()
print("✓ Base de données initialisée")

# TEST 1 : Récupérer le joueur par défaut
print("\n--- TEST 1 : get_joueur() ---")
joueur = database.get_joueur(1)
print(f"Joueur : {joueur}")
assert joueur["pseudo"] == "Joueur1", "Erreur : pseudo incorrect"
assert joueur["score"] == 0, "Erreur : score devrait être 0"
print("✓ get_joueur() fonctionne")

# TEST 2 : Mettre à jour le score
print("\n--- TEST 2 : update_score() ---")
database.update_score(10, 15, 1)
joueur = database.get_joueur(1)
print(f"Après update : {joueur}")
assert joueur["score"] == 10, "Erreur : score devrait être 10"
assert joueur["tentatives"] == 15, "Erreur : tentatives devrait être 15"
print("✓ update_score() fonctionne")

# TEST 3 : Changer le niveau
print("\n--- TEST 3 : update_niveau() ---")
database.update_niveau("difficile", 1)
joueur = database.get_joueur(1)
print(f"Après changement niveau : {joueur}")
assert joueur["niveau"] == "difficile", "Erreur : niveau devrait être 'difficile'"
print("✓ update_niveau() fonctionne")

# TEST 4 : Ajouter des tentatives
print("\n--- TEST 4 : ajouter_tentative() ---")
database.ajouter_tentative("cat", "chat", True, "chat", 1)
database.ajouter_tentative("dog", "chiot", False, "chien", 1)
database.ajouter_tentative("house", "maison", True, "maison", 1)
print("✓ 3 tentatives ajoutées")

# TEST 5 : Récupérer l'historique
print("\n--- TEST 5 : get_historique() ---")
historique = database.get_historique(1, 5)
print(f"Historique (limité à 5) : ")
for tentative in historique:
    print(f"  - {tentative['mot']} → {tentative['proposition']} : {'✓' if tentative['correct'] else '✗'}")

assert len(historique) == 3, "Erreur : devrait y avoir 3 tentatives"
assert historique[0]["mot"] == "house", "Erreur : la plus récente devrait être 'house'"
assert historique[1]["correct"] == False, "Erreur : 'dog' devrait être incorrect"
assert isinstance(historique[0]["correct"], bool), "Erreur : 'correct' devrait être un bool"
print("✓ get_historique() fonctionne")

# TEST 6 : Réinitialiser le joueur
print("\n--- TEST 6 : reset_joueur() ---")
database.reset_joueur(1)
joueur = database.get_joueur(1)
historique = database.get_historique(1, 5)
print(f"Après reset : {joueur}")
print(f"Historique après reset : {historique}")
assert joueur["score"] == 0, "Erreur : score devrait être 0"
assert joueur["tentatives"] == 0, "Erreur : tentatives devrait être 0"
assert len(historique) == 0, "Erreur : historique devrait être vide"
print("✓ reset_joueur() fonctionne")

print("\n" + "="*50)
print("🎉 TOUS LES TESTS SONT PASSÉS !")
print("="*50)
print("\nTu peux maintenant intégrer database.py dans main.py")
