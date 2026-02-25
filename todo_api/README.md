# 📋 TODO LIST API

Application de gestion de tâches (Todo List) avec :
- Backend : FastAPI + SQLite
- Frontend : HTML/CSS/JavaScript vanilla

## 🚀 Installation

1. Assure-toi d'être dans le bon dossier :
```bash
cd d:\code\translate_game\todo_api
```

2. Active ton environnement virtuel (si ce n'est pas déjà fait) :
```bash
..\\.venv\Scripts\activate
```

3. Lance le serveur :
```bash
python -m uvicorn main:app --reload
```

4. Ouvre `index.html` dans ton navigateur

## 📚 Documentation

- **Guide de révision :** Voir `../REVISION.md`
- **Consignes du projet :** Voir `CONSIGNES.md`
- **API Documentation :** http://localhost:8000/docs (une fois le serveur lancé)

## 📁 Structure du projet

```
todo_api/
├── main.py         # Backend FastAPI
├── database.py     # Gestion de la base de données SQLite
├── index.html      # Frontend
├── todos.db        # Base de données (créé automatiquement)
└── README.md       # Ce fichier
```

## ✅ Fonctionnalités à implémenter

- [ ] Connexion à la base de données
- [ ] Création de la table `tasks`
- [ ] Routes GET/POST/PUT/DELETE
- [ ] Affichage des tâches
- [ ] Ajout d'une tâche
- [ ] Marquer une tâche comme terminée
- [ ] Supprimer une tâche

## 🎯 Objectif

Réviser et mettre en pratique :
- FastAPI (routes, modèles Pydantic)
- SQLite (CRUD complet)
- JavaScript (fetch, DOM, événements)
- Communication Frontend-Backend

## 🆘 Aide

Si tu bloques :
1. Consulte `../REVISION.md` pour la théorie
2. Regarde ton ancien projet `../translate_game/`
3. Teste avec `print()` et `console.log()`
4. Demande-moi des indices !

Bon courage ! 💪
