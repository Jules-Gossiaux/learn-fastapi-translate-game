# 🗺️ ROADMAP - Jeu de Traduction

**Objectif final :** Publier un jeu de traduction en ligne avec système de connexion

---

## ✅ Compétences acquises

- FastAPI (routes, CORS, Pydantic)
- SQLite (CRUD, Foreign Keys)
- JavaScript (fetch, DOM, events)
- REST API
- Multi-joueurs avec variables globales

**Projets terminés :**
1. Jeu de traduction (translate_game)
2. Todo List API (todo_api)

---

## 📋 PLAN D'ACTION

### 🔥 PHASE 1 : Fonctionnalités critiques

#### ✅ Exercice 1 : Multi-joueurs (TERMINÉ)
- [x] Routes CRUD pour joueurs
- [x] Variable globale `joueur_actif_id`
- [x] Dropdown frontend
- [x] Gestion d'état

---

#### ✅ Exercice 2 : Authentication (PRIORITÉ)
**Temps estimé :** 5-7 jours

**Tâches :**
- [ ] `POST /register` - Créer compte
- [ ] `POST /login` - Se connecter (retourne JWT)
- [ ] `GET /me` - Info user connecté
- [ ] Hash mots de passe (bcrypt)
- [ ] Middleware JWT
- [ ] Routes protégées

**Nouveaux concepts :**
- JWT (tokens)
- Password hashing
- Middleware FastAPI
- OAuth2

---

#### ✅ Exercice 3 : Leaderboard & SQL avancé
**Temps estimé :** 3-4 jours

**Tâches :**
- [✅] Route `GET /leaderboard` (TOP 10 scores)
- [✅] Statistiques par niveau (GROUP BY)
- [✅] Table `mots` en base de données
- [✅] Filtres et recherche

**Nouveaux concepts :**
- ORDER BY, LIMIT
- GROUP BY, COUNT, AVG
- JOINs multiples

---

#### ✅ Exercice 4 : Gestion d'erreurs
**Temps estimé :** 2-3 jours

**Tâches :**
- [✅] HTTPException dans routes
- [✅] Codes HTTP corrects (404, 400, 500)
- [✅] try/catch frontend
- [✅] Messages d'erreur clairs
- [✅] Validation Pydantic avancée

**Nouveaux concepts :**
- HTTPException
- Status codes
- Error handling

---

### 🚀 PHASE 2 : Préparer la publication

#### 🎯 Exercice 5 : Clean Architecture
**Temps estimé :** 1 semaine

**Tâches :**
- [ ] Séparer routes/services/repositories
- [ ] Configuration centralisée (.env)
- [ ] Logging
- [ ] Code propre et maintenable

**Structure cible :**
```
app/
├── routes/
├── services/
├── repositories/
├── models/
└── config.py
```

---

#### 🎯 Exercice 6 : Tests (optionnel mais recommandé)
**Temps estimé :** 1 semaine

**Tâches :**
- [ ] pytest
- [ ] Tests unitaires (database)
- [ ] Tests d'intégration (routes)
- [ ] Coverage > 80%

---

#### 🎯 Exercice 7 : Déploiement 🌐
**Temps estimé :** 4-6 jours

**Tâches :**
- [ ] Variables d'environnement
- [ ] Dockerfile
- [ ] Déployer sur Render/Railway (gratuit)
- [ ] HTTPS
- [ ] Domaine

**🎉 → JEU PUBLIÉ !**

---

### 💎 PHASE 3 : Améliorations post-publication

#### 🎯 Exercice 8 : Upload de fichiers
**Temps estimé :** 3-4 jours

**Tâches :**
- [ ] Upload dictionnaire CSV/JSON
- [ ] Export historique
- [ ] Validation fichiers

---

#### 🎯 Exercice 9 : Phrases complexes
**Temps estimé :** 1-2 jours

**Tâches :**
- [ ] Traduire phrases au lieu de mots
- [ ] Système de scoring adapté
- [ ] Difficulté progressive

---

#### 🎯 Exercice 10 : API externe
**Temps estimé :** 4-5 jours

**Tâches :**
- [ ] Intégrer API traduction (LibreTranslate)
- [ ] Vérification automatique
- [ ] Cache résultats
- [ ] Gestion rate limits

---

### 🌟 PHASE 4 : Optionnel (si motivation)

#### WebSockets (temps réel)
- Mode 1v1 en direct
- Chat
- Notifications live

#### Frontend moderne
- React/Vue/Svelte
- Build optimisé

#### Autres frameworks
- Flask ou Django (pour comparer)

---

## 📅 Timeline estimé

**Version 1 (MVP avec auth) :** 2-3 semaines  
**Version 2 (en ligne) :** 3-4 semaines  
**Version 3 (features avancées) :** 2+ mois

---

## 🎯 Prochaine étape

**Exercice 2 : Authentication** ← Commence ici !

**Statut :** Phase 1 en cours  
**Dernière mise à jour :** 14 février 2026

---

**💡 Note :** Ordre flexible selon tes besoins. L'important = avancer régulièrement !
