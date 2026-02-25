# main.py - Backend du jeu de traduction
# Pour lancer le serveur : .venv\Scripts\python.exe -m uvicorn main:app --reload

from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
import database as db
from fastapi import HTTPException
from models import ChangeLevel, GuessCreate, UserRegister
from auth import get_current_user, create_access_token


# ============================================
# CONFIGURATION DU SERVEUR
# ============================================

app = FastAPI(title="Jeu de Traduction API")
DATA_FILE = "game_data.json"



# Configuration CORS : permet au frontend (HTML/JavaScript) de communiquer avec le backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Accepte toutes les origines (pour le développement)
    allow_credentials=True,
    allow_methods=["*"],  # Accepte toutes les méthodes (GET, POST, etc.)
    allow_headers=["*"],  # Accepte tous les headers
)




    
# ============================================
# ROUTES DE L'API
# ============================================

@app.post("/users")
def register(user: UserRegister):
    if db.get_user_by_username(user.username):
            raise HTTPException(
            status_code=400,
            detail="Ce username est déjà pris"
        )
    else: 
        db.create_user(user.username, user.password)
        return {"message": f"Joueur {user.username} créé"}
    
@app.post("/auth/login")
def login(user: UserRegister):
    user_data = db.get_user_by_username(user.username)
    if user_data is None: 
        raise HTTPException(
            status_code=401,
            detail="Nom d'utilisateur ou mot de passe incorrect"
        )
    
    hashed_password = user_data["password"]
    print(hashed_password)
    if db.verify_password(user.password, hashed_password):
        token = create_access_token(user_data["id"], user_data["username"])
        
        return {"username": user.username, "user_id": user_data["id"], "token": token, "token_type": "Bearer", "level": user_data["level"]}
    else: 
        raise HTTPException(
            status_code=401,
            detail="Nom d'utilisateur ou mot de passe incorrect"
        )
        
        

@app.patch("/users/{user_id}/level")
def change_level(user_id: int, data: ChangeLevel, current_user = Depends(get_current_user)):
    
    if user_id == current_user["id"]:
        db.change_level(user_id, data.level)
        return {"message": f"le joueur {user_id} jouera maintenant avec le niveau {data.level}"}
    else:
        raise HTTPException(
            status_code=403,
            detail="Tu n'as pas l'autorisation de modifier le level de ce user"
        )
        



@app.get("/users/{username}")
def get_user(username: str, current_user = Depends(get_current_user)):
    if username == current_user["username"]:
        # Retourner user sans le password
        user_data = db.get_user_by_username(username)
        return {
            "id": user_data["id"],
            "username": user_data["username"],
            "score": user_data["score"],
            "attempts": user_data["attempts"],
            "level": user_data["level"]
        }
    else:
        raise HTTPException(
            status_code=403,
            detail="Tu n'as pas l'autorisation d'accéder aux données de cet utilisateur"
        )

@app.get("/words/{language}/{level}")
def get_random_word(language: str, level: str):
    random_word = db.get_random_word(language, level)
    if random_word is None:
        raise HTTPException(
            status_code=404,
            detail="Aucun mot n'a été trouvé correspondant à vos critères"
        )
    else:
        return random_word


@app.post("/guesses")
def add_attemp(guess: GuessCreate, current_user = Depends(get_current_user)):
    if current_user["id"] == guess.user_id:
        db.add_attemp(guess.user_id, guess.word_id, guess.guess, guess.is_correct, guess.date)
        return {"message": f"Le user {guess.user_id} a bien une tentative de plus à son actif"}
    else: 
        raise HTTPException(
            status_code=403,
            detail="Tu n'as pas l'autorisation d'ajouter une tentative à cet utilisateur"
        )
        
@app.get("/guesses/{user_id}")
def get_guesses(user_id: int, current_user = Depends(get_current_user)):
    if user_id == current_user["id"]:
        return db.get_guesses(user_id, limit=5)
    else:
        raise HTTPException(
            status_code=403,
            detail="tu n'as pas l'autorisation de voir l'historique, connecte-toi"
        )
        
        
@app.get("/statistics/{user_id}")
def get_statistics(user_id: int, current_user = Depends(get_current_user)): 
    if user_id == current_user["id"]:
        return db.get_statistics(user_id)
    else: 
        raise HTTPException(
            status_code=403,
            detail="Connectez-vous"
        )
@app.get("/statistics/{user_id}/table")
def get_statistics_table(user_id: int, current_user = Depends(get_current_user)): 
    if user_id == current_user["id"]:
        return db.statistics_table(user_id)
    else: 
        raise HTTPException(
            status_code=403,
            detail="Connectez-vous"
        )

@app.delete("/users/{user_id}/reset")
def reset_score(user_id: int, current_user = Depends(get_current_user)):
    if user_id == current_user["id"]:    
        db.reset_user(user_id)
        return {"message": "Le score et les tentatives sont remises à 0"}
    else:
        raise HTTPException(
            status_code=403,
            detail="Vous n'avez pas l'autorisation"
        )


@app.get("/leaderboard")
def leaderboard(level: str = None):
    return db.leaderboard(level)

# ============================================
# ROUTE D'INFORMATION
# ============================================

@app.get("/")
def root():
    """
    Page d'accueil de l'API
    
    Returns:
        dict: Informations sur l'API et routes disponibles
    """
    return {
        "message": "Bienvenue sur l'API du jeu de traduction !",
        "routes": {
            "GET /mot-aleatoire": "Obtenir un mot aléatoire à traduire",
            "POST /verifier": "Vérifier une traduction",
            "GET /score": "Consulter le score actuel",
            "GET /reset": "Réinitialiser le score",
            "GET /docs": "Documentation interactive de l'API"
        }
    }
