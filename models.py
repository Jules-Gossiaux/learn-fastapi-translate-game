# ============================================
# MODÈLES DE DONNÉES
# ============================================

from pydantic import BaseModel, field_validator


class Verification(BaseModel):
    """Modèle pour vérifier une traduction"""
    mot_anglais: str      # Le mot en anglais à traduire
    proposition: str      # La traduction proposée par l'utilisateur

class ChangeLevel(BaseModel):
    level: str
    @field_validator("level")
    @classmethod
    def level_valid(cls, v):
        if v not in ["facile", "moyen", "difficile"]:
            raise ValueError("Le choix du level n'est pas bon")
        return v
    
class UserRegister(BaseModel):
    username: str
    password: str
    
    @field_validator("username")
    @classmethod
    def username_valid(cls, v):
        if " " in v:
            raise ValueError("Pas d'espace dans le username")
        if len(v) < 3 or len(v) > 20:
            raise ValueError("La longueur du username doit être comprise entre 3 et 20 caractères")
        return v
    @field_validator("password")
    @classmethod
    def password_valid(cls, v):
        if len(v) < 6:
            raise ValueError("le password doit faire au minimum 6 caracatères")
        return v
class GuessCreate(BaseModel):
    user_id: int
    word_id: int
    guess: str
    is_correct: bool
    date: str
