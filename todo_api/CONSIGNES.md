# 📋 TODO LIST API - Consignes du projet

## 🎯 Objectif

Créer une **API de Todo List complète** avec :
- Backend FastAPI
- Base de données SQLite
- Frontend HTML/CSS/JavaScript

**Durée estimée :** 1-2 jours

---

## 📦 Ce que tu dois coder

### ✅ PARTIE 1 : Base de données (`database.py`)

**Créer 5 fonctions :**

1. `get_connexion()` → Retourne une connexion SQLite
2. `init_db()` → Crée la table `tasks`
3. `get_all_tasks()` → Récupère toutes les tâches
4. `add_task(title)` → Ajoute une tâche
5. `update_task(task_id, completed)` → Met à jour le statut (terminé ou non)
6. `delete_task(task_id)` → Supprime une tâche

**Structure de la table `tasks` :**
```sql
CREATE TABLE tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    completed INTEGER DEFAULT 0,
    created_at TEXT NOT NULL
)
```

---

### ✅ PARTIE 2 : Backend (`main.py`)

**Créer 5 routes :**

1. `GET /tasks` → Retourne toutes les tâches
2. `POST /tasks` → Ajoute une nouvelle tâche
3. `PUT /tasks/{task_id}` → Marque une tâche comme terminée/non terminée
4. `DELETE /tasks/{task_id}` → Supprime une tâche
5. `GET /` → Page d'accueil avec infos sur l'API

**Modèle Pydantic à créer :**
```python
class Task(BaseModel):
    title: str
    completed: bool = False
```

---

### ✅ PARTIE 3 : Frontend (`index.html`)

**Interface simple avec :**

1. **Un formulaire** pour ajouter une tâche
   - Input texte
   - Bouton "Ajouter"

2. **Une liste de tâches** affichant :
   - Le titre de la tâche
   - Une checkbox pour marquer comme terminé
   - Un bouton "Supprimer"

3. **Fonctionnalités JavaScript :**
   - Charger les tâches au démarrage
   - Ajouter une tâche
   - Cocher/décocher une tâche (met à jour en base)
   - Supprimer une tâche

---

## 🎨 Design minimaliste suggéré

```
┌──────────────────────────────────────┐
│        📋 MA TODO LIST               │
├──────────────────────────────────────┤
│  [___________] [Ajouter]             │
├──────────────────────────────────────┤
│  ☐ Faire les courses      [Supprimer]│
│  ☑ Apprendre FastAPI      [Supprimer]│
│  ☐ Créer un projet        [Supprimer]│
└──────────────────────────────────────┘
```

---

## 📝 Étapes recommandées

### Jour 1 : Backend + Base de données

1. ✅ Créer `database.py` avec les 6 fonctions
2. ✅ Tester les fonctions dans un petit script Python
3. ✅ Créer `main.py` avec les 5 routes
4. ✅ Tester les routes sur `http://localhost:8000/docs`

### Jour 2 : Frontend

5. ✅ Créer `index.html` avec la structure HTML/CSS
6. ✅ Ajouter le JavaScript pour :
   - Charger les tâches
   - Ajouter une tâche
   - Marquer comme terminé
   - Supprimer

---

## 🆘 Si tu bloques

**N'hésite pas à me demander :**
- "Comment faire X ?"
- "Pourquoi ça ne marche pas ?"
- "Un indice pour Y ?"

**Mais essaie d'abord :**
1. Relis `REVISION.md`
2. Regarde ton ancien projet `translate_game/`
3. Teste avec `print()` et `console.log()`

---

## 🎯 Résultat attendu

À la fin, tu dois avoir :
- ✅ Une API qui fonctionne (teste avec `/docs`)
- ✅ Une base de données qui persiste (redémarre le serveur, les tâches restent)
- ✅ Un frontend fonctionnel (ajouter/supprimer/cocher des tâches)

---

## 🚀 Bonus (si tu as le temps)

- [ ] Ajouter une route `GET /tasks/{task_id}` → Récupérer une seule tâche
- [ ] Ajouter une date d'échéance pour chaque tâche
- [ ] Trier les tâches (terminées en bas)
- [ ] Ajouter un compteur de tâches terminées/totales
- [ ] Styliser joliment avec CSS

---

## 🎓 Ce que tu vas réviser

- ✅ Routes FastAPI (GET, POST, PUT, DELETE)
- ✅ SQLite (CREATE, INSERT, SELECT, UPDATE, DELETE)
- ✅ Pydantic (validation de données)
- ✅ Fetch API (JavaScript)
- ✅ Manipulation du DOM
- ✅ CORS
- ✅ Structure de projet

---

**Bon courage ! Tu as tout ce qu'il faut dans `REVISION.md` 💪**

**Commence par `database.py`, puis `main.py`, puis `index.html` !**
