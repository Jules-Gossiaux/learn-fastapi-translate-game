# 📚 GUIDE DE RÉVISION - Backend & Frontend

## 🐍 PARTIE 1 : FastAPI (Backend Python)

### 1️⃣ Structure minimale d'un serveur FastAPI

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# CORS : permet au frontend de communiquer avec le backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Route GET simple
@app.get("/hello")
def dire_bonjour():
    return {"message": "Bonjour !"}
```

**Pour lancer le serveur :**
```bash
python -m uvicorn main:app --reload
```

---

### 2️⃣ Créer une route GET (récupérer des données)

```python
@app.get("/chemin")
def nom_fonction():
    return {"cle": "valeur"}
```

**Exemple concret :**
```python
@app.get("/users")
def get_users():
    return {"users": ["Alice", "Bob", "Charlie"]}
```

**Accès :** `http://localhost:8000/users`

---

### 3️⃣ Créer une route GET avec paramètre dans l'URL

```python
@app.get("/user/{user_id}")
def get_user(user_id: int):
    return {"id": user_id, "name": "Alice"}
```

**Accès :** `http://localhost:8000/user/5`

---

### 4️⃣ Créer une route POST (envoyer des données)

**Étape 1 : Créer un modèle Pydantic**
```python
from pydantic import BaseModel

class Task(BaseModel):
    title: str
    completed: bool = False
```

**Étape 2 : Créer la route**
```python
@app.post("/tasks")
def create_task(task: Task):
    # task.title → accéder au champ title
    # task.completed → accéder au champ completed
    return {"message": "Tâche créée", "task": task.title}
```

---

### 5️⃣ Routes PUT et DELETE

```python
@app.put("/tasks/{task_id}")
def update_task(task_id: int):
    return {"message": f"Tâche {task_id} mise à jour"}

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    return {"message": f"Tâche {task_id} supprimée"}
```

---

## 🗄️ PARTIE 2 : SQLite (Base de données)

### 1️⃣ Se connecter à la base de données

```python
import sqlite3

def get_connexion():
    connexion = sqlite3.connect("database.db")
    connexion.execute("PRAGMA foreign_keys = ON")  # Active les clés étrangères
    return connexion
```

---

### 2️⃣ Créer une table

```python
def init_db():
    connexion = get_connexion()
    curseur = connexion.cursor()
    
    curseur.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            completed INTEGER DEFAULT 0,
            created_at TEXT NOT NULL
        )
    """)
    
    connexion.commit()
    connexion.close()
```

---

### 3️⃣ Insérer des données (INSERT)

```python
def add_task(title):
    connexion = get_connexion()
    curseur = connexion.cursor()
    
    curseur.execute(
        "INSERT INTO tasks (title, completed, created_at) VALUES (?, ?, ?)",
        (title, 0, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    )
    
    connexion.commit()
    connexion.close()
```

**IMPORTANT :** Toujours utiliser `?` et un tuple pour éviter l'injection SQL !

---

### 4️⃣ Récupérer des données (SELECT)

**Récupérer toutes les lignes :**
```python
def get_all_tasks():
    connexion = get_connexion()
    curseur = connexion.cursor()
    
    curseur.execute("SELECT id, title, completed FROM tasks")
    rows = curseur.fetchall()  # Liste de tuples
    
    connexion.close()
    
    # Transformer en liste de dictionnaires
    tasks = []
    for row in rows:
        tasks.append({
            "id": row[0],
            "title": row[1],
            "completed": bool(row[2])  # Convertir 0/1 en False/True
        })
    
    return tasks
```

**Récupérer une seule ligne :**
```python
def get_task(task_id):
    connexion = get_connexion()
    curseur = connexion.cursor()
    
    curseur.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
    row = curseur.fetchone()  # Un seul tuple
    
    connexion.close()
    
    if row:
        return {"id": row[0], "title": row[1], "completed": bool(row[2])}
    return None
```

---

### 5️⃣ Mettre à jour des données (UPDATE)

```python
def update_task(task_id, completed):
    connexion = get_connexion()
    curseur = connexion.cursor()
    
    curseur.execute(
        "UPDATE tasks SET completed = ? WHERE id = ?",
        (1 if completed else 0, task_id)
    )
    
    connexion.commit()
    connexion.close()
```

---

### 6️⃣ Supprimer des données (DELETE)

```python
def delete_task(task_id):
    connexion = get_connexion()
    curseur = connexion.cursor()
    
    curseur.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    
    connexion.commit()
    connexion.close()
```

---

## 🌐 PARTIE 3 : JavaScript (Frontend)

### 1️⃣ Faire une requête GET avec fetch()

```javascript
async function getTasks() {
    const response = await fetch("http://localhost:8000/tasks");
    const data = await response.json();
    console.log(data);  // Affiche les données
    return data;
}
```

---

### 2️⃣ Faire une requête POST avec fetch()

```javascript
async function createTask(title) {
    const response = await fetch("http://localhost:8000/tasks", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            title: title,
            completed: false
        })
    });
    
    const data = await response.json();
    return data;
}
```

---

### 3️⃣ Faire une requête PUT

```javascript
async function updateTask(taskId, completed) {
    const response = await fetch(`http://localhost:8000/tasks/${taskId}`, {
        method: "PUT",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            completed: completed
        })
    });
    
    const data = await response.json();
    return data;
}
```

---

### 4️⃣ Faire une requête DELETE

```javascript
async function deleteTask(taskId) {
    const response = await fetch(`http://localhost:8000/tasks/${taskId}`, {
        method: "DELETE"
    });
    
    const data = await response.json();
    return data;
}
```

---

### 5️⃣ Manipuler le DOM (afficher des données)

```javascript
function afficherTasks(tasks) {
    const container = document.getElementById("task-list");
    container.innerHTML = "";  // Vider le conteneur
    
    tasks.forEach(task => {
        const div = document.createElement("div");
        div.textContent = task.title;
        container.appendChild(div);
    });
}
```

---

### 6️⃣ Gérer un événement (clic sur un bouton)

```javascript
document.getElementById("add-button").addEventListener("click", async () => {
    const input = document.getElementById("task-input");
    const title = input.value;
    
    await createTask(title);
    input.value = "";  // Vider l'input
    
    // Recharger la liste
    const tasks = await getTasks();
    afficherTasks(tasks);
});
```

---

## 🔄 PARTIE 4 : Lier Frontend et Backend

### Workflow complet :

1. **Backend** : Créer la route `/tasks` qui retourne les données de la DB
2. **Frontend** : Appeler `fetch("http://localhost:8000/tasks")`
3. **Frontend** : Afficher les données dans le HTML

**Exemple complet :**

**Backend (main.py) :**
```python
import database

@app.get("/tasks")
def get_tasks():
    tasks = database.get_all_tasks()
    return {"tasks": tasks}
```

**Frontend (JavaScript) :**
```javascript
async function chargerTasks() {
    const response = await fetch("http://localhost:8000/tasks");
    const data = await response.json();
    afficherTasks(data.tasks);
}

// Appeler au chargement de la page
chargerTasks();
```

---

## ✅ CHECKLIST : Ce qu'il faut retenir

### Backend
- [ ] `@app.get("/route")` → Route GET
- [ ] `@app.post("/route")` → Route POST (avec BaseModel)
- [ ] `@app.put("/route/{id}")` → Route PUT
- [ ] `@app.delete("/route/{id})` → Route DELETE

### Base de données
- [ ] `sqlite3.connect()` → Connexion
- [ ] `cursor.execute()` → Exécuter une requête
- [ ] `fetchall()` → Toutes les lignes
- [ ] `fetchone()` → Une seule ligne
- [ ] `commit()` → Sauvegarder (pour INSERT/UPDATE/DELETE)
- [ ] `close()` → Fermer la connexion
- [ ] Utiliser `?` et tuples pour les paramètres

### Frontend
- [ ] `fetch(url)` → Requête GET
- [ ] `fetch(url, {method: "POST", body: ...})` → Requête POST
- [ ] `response.json()` → Récupérer les données
- [ ] `document.getElementById()` → Sélectionner un élément
- [ ] `addEventListener()` → Gérer les événements

---

## 🎯 Maintenant, ouvre `CONSIGNES.md` pour commencer le projet !
