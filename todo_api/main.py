# main.py - Backend de la Todo List API
# Pour lancer le serveur : python -m uvicorn main:app --reload

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import database as db


# ============================================
# CONFIGURATION DU SERVEUR
# ============================================

app = FastAPI(title="Todo List API")

# Configuration CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================
# MODÈLES DE DONNÉES
# ============================================
class Task(BaseModel):
    title: str
    completed: bool = False


class TaskUpdate(BaseModel):
    completed: bool   

# ============================================
# ROUTES DE L'API
# ============================================

@app.get("/")
def root():
    # Return un dict avec message et liste des routes
    return {
        "Message": "Bonjour, vous êtes sur la page d'accueil des routes de mon app de tasks",
        "routes": [
            "/",
            "/tasks",
            "/tasks (POST)",
            "/tasks/{task_id} (PUT)",
            "/tasks/{task_id} (DELETE)"
        ]
    }

# Return {"tasks": liste de toutes les tâches}
@app.get("/tasks")
def get_tasks():
    return {"tasks": db.get_all_tasks()}

# Ajoute la tâche en DB, return message de confirmation
@app.post("/tasks")
def add_task(task: Task):
    print("on ajoute une tache")
    db.add_task(task.title)
    return {"message": f"la tâche {task.title} a bien été ajoutée"}
    

# Update la tâche en DB, return message de confirmation
@app.put("/tasks/{task_id}")
def update_task(task_id: int, task_update: TaskUpdate):
    print(f"on modifie le statut de la tache {task_id}")
    db.update_task(task_id, task_update.completed)
    return {"message": f"la tâche {task_id} a bien été modifiée en {task_update.completed}"}
# Supprime la tâche de la DB, return message de confirmation


@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    db.delete_task(task_id)
    return {"message": f"la tache {task_id} a bien été supprimée"}