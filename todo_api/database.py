# database.py - Gestion de la base de données pour la Todo List
import sqlite3
from datetime import datetime

DB_FILE = "todos.db"

def get_connexion():
    # Crée et retourne une connexion SQLite
    connexion = sqlite3.connect(DB_FILE)
    connexion.execute("PRAGMA foreign_keys = ON")
    return connexion


def init_db():
    # Crée la table tasks si elle n'existe pas
    connexion = get_connexion()
    curseur = connexion.cursor()
    curseur.execute("""
                CREATE TABLE IF NOT EXISTS tasks(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    completed INTEGER DEFAULT 0,
                    created_at TEXT NOT NULL
                )
                """)
    connexion.commit()
    connexion.close()


def get_all_tasks():
    # Récupère toutes les tâches
    connexion = get_connexion()
    curseur = connexion.cursor()
    
    curseur.execute("SELECT * FROM tasks")
    content = curseur.fetchall()
    all_tasks = []
    for row in content: 
        dico = {"id": row[0], "title": row[1], "completed": bool(row[2]), "created_at": row[3]}
        all_tasks.append(dico)
    connexion.close()
    return all_tasks


def add_task(title):
    # Ajoute une nouvelle tâche
    connexion = get_connexion()
    curseur = connexion.cursor()

    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    curseur.execute("INSERT INTO tasks (title, completed, created_at) VALUES (?, ?, ?)", (title, 0, date))
    connexion.commit()
    connexion.close()


def update_task(task_id, completed):
    # Met à jour le statut d'une tâche
    connexion = get_connexion()
    curseur = connexion.cursor()
    value = 1 if completed else 0
    curseur.execute("UPDATE tasks SET completed = ? WHERE id = ?", (value, task_id))
    connexion.commit()
    connexion.close()


def delete_task(task_id):
    # Supprime une tâche
    connexion = get_connexion()
    curseur = connexion.cursor()
    
    curseur.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    connexion.commit()
    connexion.close()


# Initialise la base au chargement du module
init_db()
