# 🔐 EXERCICE 2 : Authentication

## Objectif
Créer un système de login/register avec JWT pour sécuriser une API.

---

## Packages à installer

```
pip install python-jose[cryptography] passlib[bcrypt]
```

- `python-jose` : Créer et décoder les JWT
- `passlib` : Hasher les mots de passe avec bcrypt

---

## Base de données

### Table `users`
Colonnes nécessaires :
- id (entier, auto-incrémenté, clé primaire)
- username (texte, unique, obligatoire)
- hashed_password (texte, obligatoire)
- created_at (date/heure)

Pas besoin de stocker le mot de passe en clair, juste le hash.

---

## Backend - database.py

### Fonction 1 : `create_user(username, password)`
- Hasher le password avec bcrypt
- Insérer dans la table users
- Retourner l'ID du nouvel utilisateur

### Fonction 2 : `get_user_by_username(username)`
- Chercher un user par son username
- Retourner un dictionnaire avec id, username, hashed_password
- Retourner None si pas trouvé

### Fonction 3 : `verify_password(plain_password, hashed_password)`
- Comparer le mot de passe en clair avec le hash
- Retourner True si correct, False sinon

---

## Backend - main.py

### Configuration JWT
Définir 2 constantes :
- SECRET_KEY : une clé secrète aléatoire (garder en privé)
- ALGORITHM : "HS256" (algorithme de hashage)

### Fonction utilitaire : `create_access_token(user_id, username)`
- Créer un dictionnaire avec user_id, username, et date d'expiration
- Encoder ce dictionnaire en JWT avec la SECRET_KEY
- Retourner le token

### Fonction utilitaire : `decode_token(token)`
- Décoder le JWT avec la SECRET_KEY
- Retourner les données (user_id, username)
- Gérer les erreurs (token expiré, invalide)

### Dependency : `get_current_user(token)`
- Extraire le token du header Authorization
- Décoder le token
- Récupérer l'utilisateur depuis la DB
- Retourner l'utilisateur ou erreur 401

---

## Routes à créer

### Route 1 : POST /register
- Recevoir username et password
- Vérifier que le username n'existe pas déjà
- Créer le user avec `create_user()`
- Retourner message de confirmation

### Route 2 : POST /login
- Recevoir username et password
- Récupérer le user avec `get_user_by_username()`
- Vérifier le password avec `verify_password()`
- Si ok : créer un JWT et le retourner
- Si pas ok : erreur 401

### Route 3 : GET /me (protégée)
- Utiliser la dependency `get_current_user`
- Retourner les infos du user connecté

### Route 4 : GET /protected (protégée, pour tester)
- Utiliser la dependency `get_current_user`
- Retourner un message avec le nom du user

---

## Frontend - HTML/JS

### Page de login
- Formulaire avec username et password
- Bouton "Se connecter"
- Au submit : envoyer POST /login
- Sauvegarder le token dans localStorage
- Rediriger vers la page principale

### Page de register
- Formulaire avec username et password
- Bouton "Créer un compte"
- Au submit : envoyer POST /register
- Rediriger vers login

### Toutes les requêtes protégées
- Récupérer le token depuis localStorage
- Ajouter le header Authorization: Bearer {token}
- Si erreur 401 : rediriger vers login

### Bouton logout
- Supprimer le token de localStorage
- Rediriger vers login

---

## Ordre de travail recommandé

1. Installer les packages
2. Créer la table users dans database.py
3. Coder les 3 fonctions dans database.py
4. Tester ces fonctions dans un fichier de test
5. Créer les utilitaires JWT dans main.py
6. Créer la route POST /register
7. Créer la route POST /login
8. Créer la dependency get_current_user
9. Créer les routes protégées
10. Tester toutes les routes sur /docs
11. Créer le frontend (login.html)
12. Tester le flow complet

---

## Points importants

- Ne JAMAIS stocker les mots de passe en clair
- La SECRET_KEY doit rester secrète (ne pas commit sur GitHub)
- Les tokens JWT ont une durée de vie (30 min recommandé)
- Toujours vérifier le token côté backend, jamais faire confiance au frontend
- Gérer les erreurs 401 (non autorisé) proprement

---

**Projet parallèle :** On va créer `auth_practice/` pour coder tout ça !
