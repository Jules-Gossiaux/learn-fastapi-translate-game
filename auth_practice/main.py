from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from jose import JWTError, jwt
from datetime import datetime, timedelta, UTC
import database as db

app = FastAPI(title="Auth Practice API")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================
# CONFIGURATION JWT
# ============================================
SECRET_KEY = "votre-cle-secrete-super-longue-et-aleatoire-123456789"  # À CHANGER !
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# ============================================
# MODÈLES PYDANTIC
# ============================================
class UserRegister(BaseModel):
    username: str
    password: str
# ============================================
# FONCTIONS UTILITAIRES JWT
# ============================================
def create_access_token(user_id: int, username: str):
    # Créer un dict avec user_id, username, exp (expiration)
    # Encoder avec jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
    # Retourner le token
    expire = datetime.now(UTC) + timedelta(minutes=30)
    data = {"user_id": user_id, "username": username, "exp": expire}
    token = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
    return token

def decode_token(token: str):
    # Décoder avec jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    # Gérer les erreurs (JWTError)
    # Retourner les données ou None
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("user_id")
        username = payload.get("username")
        
        if user_id is None or username is None:
            return None
        
        return {"user_id": user_id, "username": username}
    except JWTError:
        return None

# ============================================
# DEPENDENCY : Récupérer l'utilisateur connecté
# ============================================
def get_current_user(token: str = Depends(oauth2_scheme)):
    # Étape 1 : Décoder le token
    token_data = decode_token(token)
    if token_data is None:
        raise HTTPException(
            status_code=401, 
            detail="Token invalide ou expiré"
        )
    
    # Étape 2 : Récupérer le user de la DB
    user = db.get_user_by_username(token_data["username"])
    if user is None:
        raise HTTPException(
            status_code=401, 
            detail="Utilisateur introuvable"
        )
    
    # Étape 3 : Retourner le user
    return user

# ============================================
# ROUTES
# ============================================

@app.post("/register")
def register(data: UserRegister):
    # Vérifier si l'utilisateur existe déjà
    existing_user = db.get_user_by_username(data.username)
    if existing_user is not None:
        raise HTTPException(status_code=400, detail="Ce username existe déjà")
    
    # Créer le nouvel utilisateur
    user_id = db.create_user(data.username, data.password)
    return {"message": f"User {data.username} créé avec succès"}

@app.post("/login")
def login(data: UserRegister):
    # ÉTAPE 1 : Récupérer le user de la DB avec le username
    user = db.get_user_by_username(data.username)
    
    # ÉTAPE 2 : Vérifier que le user existe
    if user is None:
        raise HTTPException(status_code=401, detail="Username ou password incorrect")
    
    # ÉTAPE 3 : Vérifier le password
    # user["hashed_password"] = le hash en base
    # data.password = le password en clair envoyé par le user
    is_valid = db.verify_password(data.password, user["hashed_password"])
    
    if not is_valid:
        raise HTTPException(status_code=401, detail="Username ou password incorrect")
    
    # ÉTAPE 4 : Si on arrive ici, c'est bon ! Créer le token
    token = create_access_token(user["id"], user["username"])
    
    # ÉTAPE 5 : Retourner le token
    return {"access_token": token, "token_type": "bearer"}

@app.get("/me")
def get_me(current_user = Depends(get_current_user)):
    # Route protégée : retourner les infos du user connecté
    return {
        "id": current_user["id"],
        "username": current_user["username"],
        "created_at": current_user["created_at"]
    }


@app.get("/protected")
def protected_route(current_user = Depends(get_current_user)):
    # Route protégée pour tester
    return {
        "message": "Bravo ! Tu as accès à cette route protégée",
        "user": current_user["username"]
    }

@app.get("/")
def root():
    return {"message": "Auth Practice API"}
