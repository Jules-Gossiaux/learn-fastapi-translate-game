
# ============================================
# fonctions
# ============================================
        
from datetime import datetime, timedelta, timezone

from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt

from config import ACCESS_TOKEN_EXPIRE_HOURS, ALGORITHM, SECRET_KEY
import database as db

oauth2_scheme = HTTPBearer()


def create_access_token(user_id, username):
    payload = {
        "user_id": user_id,
        "username": username,
        "exp": datetime.now(timezone.utc) + timedelta(hours=ACCESS_TOKEN_EXPIRE_HOURS)
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token

def decode_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("user_id")
        username = payload.get("username")
        if username is None or user_id is None:
            return None
        else: 
            return {"user_id": user_id, "username": username}
    except JWTError:
        return None
    
def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(oauth2_scheme)):
    token = credentials.credentials
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