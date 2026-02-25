# main.py - Notre premier serveur !
# Pour lancer le server, voici la commande: .venv\Scripts\python.exe -m uvicorn main:app --reload

# On importe FastAPI, c'est la bibliothèque qui nous aide à créer un serveur
from fastapi import FastAPI
# Pydantic nous aide à définir la structure des données qu'on reçoit
from pydantic import BaseModel
# CORSMiddleware permet au frontend de parler au backend
from fastapi.middleware.cors import CORSMiddleware

import random

# On crée notre "application" serveur
# C'est comme ouvrir un restaurant vide pour l'instant
app = FastAPI()

# Configuration CORS : permet au navigateur d'envoyer des requêtes au backend
# Sans ça, le navigateur bloque les requêtes pour raisons de sécurité
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Accepte toutes les origines (pour l'apprentissage)
    allow_credentials=True,
    allow_methods=["*"],  # Accepte GET, POST, etc.
    allow_headers=["*"],  # Accepte tous les headers
)


# ============================================
# MODÈLE DE DONNÉES (ce qu'on va recevoir)
# ============================================
# Ceci définit la STRUCTURE des données qu'on attend
# C'est comme un "formulaire" : on dit quels champs on veut recevoir
class Traduction(BaseModel):
    phrase_anglais: str  # Le texte en anglais que l'utilisateur envoie


# Modèle pour vérifier une traduction
class Verification(BaseModel):
    mot_anglais: str      # Le mot en anglais
    proposition: str      # La traduction proposée par l'utilisateur


# ============================================
# STOCKAGE EN MÉMOIRE (données temporaires)
# ============================================
# On crée une variable qui va stocker le score
# Attention : si on redémarre le serveur, le score repart à 0
score_joueur = 0

# Un dictionnaire avec les bonnes traductions
# C'est notre "base de données" pour l'instant (très simple)
dictionnaire = {
    "hello": "bonjour",
    "cat": "chat",
    "dog": "chien",
    "house": "maison",
    "book": "livre",
    "water": "eau",
    "sun": "soleil",
    "tree": "arbre",
    "car": "voiture",
    "apple": "pomme"
}

liste_courses = []

# ROUTE 1 : La page d'accueil
# Quand quelqu'un visite "http://localhost:8000/", il reçoit ce message
@app.get("/")
def accueil():
    return {"message": "Bienvenue sur le serveur de traduction !"}


# ROUTE 2 : Une page "à propos"
# Quand quelqu'un visite "http://localhost:8000/about", il reçoit ce message
@app.get("/about")
def a_propos():
    return {"info": "Ceci est un jeu de traduction pour apprendre le backend"}


# ROUTE 3 : Une page qui dit bonjour
# Quand quelqu'un visite "http://localhost:8000/hello", il reçoit ce message
@app.get("/hello")
def dire_bonjour():
    return {"Hello": "Bonjour, utilisateur !"}


# ROUTE 4 : Le score actuel
@app.get("/score")
def get_score():
    # On renvoie le score actuel du joueur
    return {"score": score_joueur}


# ROUTE RESET : Réinitialiser le score
@app.get("/reset")
def reset():
    global score_joueur  # On accède à la variable globale
    score_joueur = 0     # On remet le score à zéro
    return {"message": "Score réinitialisé !", "score": score_joueur}


# ROUTE MOT ALÉATOIRE : Obtenir un mot à traduire
@app.get("/mot-aleatoire")
def mot_aleatoire():
    # On transforme les clés du dictionnaire en liste
    mots_disponibles = list(dictionnaire.keys())
    # On choisit un mot au hasard dans cette liste
    mot_choisi = random.choice(mots_disponibles)
    # On renvoie le mot
    return {"mot": mot_choisi}

    
# ROUTE 5 : Une route avec un PARAMÈTRE
# {nom} est une variable : elle change selon ce que l'utilisateur écrit dans l'URL
# Par exemple : /hello/Alice ou /hello/Bob
# IMPORTANT : Cette route est APRÈS /score car elle a un paramètre
@app.get("/hello/{nom}")
def dire_bonjour_personnalise(nom: str):
    # La valeur de {nom} dans l'URL arrive ici dans la variable "nom"
    return {"message": f"Bonjour {nom} ! Bienvenue sur le serveur !"}


# ROUTE 6 : Calculer l'âge (exercice réussi !)
@app.get("/age/{annee_naissance}")
def get_age(annee_naissance: int):
    age = 2026 - annee_naissance
    # On renvoie un dictionnaire avec une clé "age" et la valeur calculée
    return {"age": age, "message": f"Tu as {age} ans !"}


# ============================================
# ROUTE 8 : Vérifier une traduction (le cœur du jeu !)
# ============================================
@app.post("/verifier")
def verifier_traduction(donnees: Verification):
    # On utilise "global" pour modifier la variable score_joueur qui est en dehors de la fonction
    global score_joueur
    
    mot_anglais = donnees.mot_anglais.lower()
    proposition = donnees.proposition.lower()
    
    # On vérifie si le mot existe dans notre dictionnaire
    if mot_anglais not in dictionnaire:
        return {
            "status": "erreur",
            "message": f"Le mot '{mot_anglais}' n'est pas dans le dictionnaire"
        }
    
    # On récupère la bonne traduction
    bonne_traduction = dictionnaire[mot_anglais]
    
    # On compare avec la proposition de l'utilisateur
    if proposition == bonne_traduction:
        score_joueur += 1  # On augmente le score !
        return {
            "status": "correct",
            "message": "Bravo ! C'est correct !",
            "score": score_joueur
        }
    else:
        return {
            "status": "incorrect",
            "message": f"Dommage ! La bonne réponse était : {bonne_traduction}",
            "score": score_joueur
        }
        

class PersonneAge(BaseModel):
    prenom: str
    annee_naissance: int

@app.post("/dire-age")
def dire_age(personne: PersonneAge):
    age = 2026-personne.annee_naissance
    if age<0:
        return {"message d'erreur": f"ce n'est pas possible dêtre né en {personne.annee_naissance}"}
    elif age>=0:
        return {"message": f"{personne.prenom} a {age}"}
    
    
    
class Calcul(BaseModel):
    nombre1: float
    nombre2: float
    operation: str
    
    
@app.post("/calcul")
def calcul(params: Calcul):
    if params.operation == "addition":
        return {"reponse": f"voici la somme de {params.nombre1} et de {params.nombre2}: {params.nombre1 + params.nombre2}"}
    if params.operation == "multiplication": 
        return {"reponse": f"voici la multiplication de {params.nombre1} et de {params.nombre2}: {params.nombre1 * params.nombre2}"}

    
    
class Article(BaseModel): 
    nom: str
    
@app.post("/ajouter-course")
def ajouter_course(article: Article):
    global liste_courses
    liste_courses.append(article.nom)
    return {"message": f"{article.nom} ajouté !", "total": len(liste_courses)}

@app.get("/afficher-liste-course")
def afficher_liste():
    return {"courses": liste_courses, "total": len(liste_courses)}





# Fonctionnalités :

# POST /creer-utilisateur : crée un nouvel utilisateur avec un score à 0
# POST /ajouter-points : ajoute des points à un utilisateur
# GET /classement : affiche tous les utilisateurs avec leurs scores


utilisateurs = []

class Users(BaseModel): 
    nom: str
    score: int
    
@app.post("/nouvel-utilisateur")
def ajouterUtilisateur(user: Users):
    global utilisateurs
    utilisateur = {"nom": user.nom, "score": user.score}
    utilisateurs.append(utilisateur)
    return {"message": f"{utilisateur} est de la partie"}
    
@app.get("/affiche-utilisateurs")
def afficheUtilisateurs():
    return {"utilisateurs": utilisateurs}

class User(BaseModel):
    name: str
    add_score: int
    
    
@app.post("/ajouter-score")
def ajouteScore(user: User):
    global utilisateurs
    
    # On cherche l'utilisateur
    for utilisateur in utilisateurs:
        if utilisateur["nom"] == user.name:
            utilisateur["score"] += user.add_score
            return {"message": f"Score mis à jour ! {user.name} a maintenant {utilisateur['score']} points"}
    
    # Si on arrive ici, c'est que l'utilisateur n'existe pas
    return {"message": f"l'utilisateur {user.name} n'existe pas"}
    