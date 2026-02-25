# Synthèse : Authentification JWT

## 🎯 Objectif global
Permettre aux utilisateurs de créer un compte, se connecter, et accéder à des routes protégées sans que leur mot de passe ne soit stocké en clair.

---

## 📋 Les 3 grandes étapes

### 1️⃣ **INSCRIPTION (Register)**
**Problème** : L'utilisateur crée un compte  
**Solution** : Hasher le mot de passe avant de le stocker

**Logique :**
- User envoie `username` + `password` en clair
- Serveur vérifie que le username n'existe pas déjà
- Serveur **hash** le password avec un algorithme sécurisé (pbkdf2_sha256)
- Serveur stocke `username` + `hashed_password` dans la base de données
- Le mot de passe en clair **n'est jamais stocké**

**Pourquoi hasher ?**  
Si quelqu'un vole la base de données, il ne peut pas lire les mots de passe originaux.

---

### 2️⃣ **CONNEXION (Login)**
**Problème** : L'utilisateur veut prouver son identité  
**Solution** : Vérifier le mot de passe et donner un token JWT

**Logique :**
- User envoie `username` + `password` en clair
- Serveur récupère le user de la DB avec ce username
- Serveur **compare** le password envoyé avec le hash stocké (vérification bcrypt/pbkdf2)
- Si ça correspond → Serveur **crée un token JWT** contenant :
  - `user_id`
  - `username`
  - `exp` (date d'expiration : dans 30 minutes)
- Serveur **signe** ce token avec une clé secrète
- Serveur **renvoie** le token au client
- Client **stocke** le token dans `localStorage`

**Pourquoi un token ?**  
Le client n'a pas besoin de renvoyer username/password à chaque requête. Le token prouve l'identité.

---

### 3️⃣ **ACCÈS AUX ROUTES PROTÉGÉES**
**Problème** : Seuls les utilisateurs connectés peuvent accéder à certaines routes  
**Solution** : Vérifier le token à chaque requête

**Logique :**
- User envoie une requête vers une route protégée (ex: `/me`)
- User **inclut le token** dans le header HTTP `Authorization: Bearer <token>`
- Serveur **extrait** le token du header
- Serveur **décode** le token avec la clé secrète
- Serveur **vérifie** :
  - Le token est-il valide ? (signature correcte)
  - Le token est-il expiré ? (exp < maintenant)
  - L'utilisateur existe-t-il encore dans la DB ?
- Si toutes les vérifications passent → **Accès autorisé**
- Sinon → **Erreur 401 Unauthorized**

**Pourquoi vérifier à chaque fois ?**  
Un token peut expirer, ou l'utilisateur peut avoir été supprimé de la DB.

---

## 🔐 Concepts clés

### Password Hashing
- **Hash** = Transformation irréversible d'un mot de passe
- Exemple : `"jules"` → `"$pbkdf2-sha256$29000$..."`
- On ne peut **pas** retrouver le mot de passe original à partir du hash
- On peut seulement **vérifier** si un mot de passe correspond au hash

### JWT (JSON Web Token)
- **Format** : `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxLCJ1c2VybmFtZSI6Im5pbm9uIiwiZXhwIjoxNzQwMDAwMH0.signature`
- **3 parties** : Header + Payload + Signature
- **Payload** contient les données (user_id, username, exp)
- **Signature** prouve que le token n'a pas été modifié
- **Expiration** : Le token devient invalide après 30 minutes

### localStorage
- **Emplacement** : Stockage dans le navigateur du client
- **Utilisation** : `localStorage.setItem("token", "eyJhbGc...")` après login
- **Lecture** : `localStorage.getItem("token")` avant chaque requête protégée
- **Suppression** : `localStorage.removeItem("token")` au logout

### Routes protégées
- **Définition** : Routes qui nécessitent un token valide
- **Mécanisme** : `Depends(get_current_user)` dans FastAPI
- **Fonctionnement** : La fonction `get_current_user()` est appelée **automatiquement avant** la route
- Si le token est invalide → Exception 401 **avant même** d'entrer dans la route

---

## 🔄 Flow complet (de bout en bout)

### Scénario : Alice veut jouer au jeu

**1. Inscription**
```
Alice → Formulaire (ninon / secret123)
      → POST /register
      → Serveur hash "secret123"
      → Serveur stocke dans DB : (ninon, $pbkdf2-sha256$...)
      → Réponse : "User ninon créé avec succès"
```

**2. Connexion**
```
Alice → Formulaire (ninon / secret123)
      → POST /login
      → Serveur récupère hash de ninon dans DB
      → Serveur vérifie "secret123" contre le hash → ✅ Match
      → Serveur crée JWT avec {user_id: 1, username: ninon, exp: 30 min}
      → Réponse : {access_token: "eyJhbGc...", token_type: "bearer"}
      → Alice stocke le token dans localStorage
```

**3. Accès à une route protégée**
```
Alice → Clique sur "Voir mon profil"
      → GET /me avec header "Authorization: Bearer eyJhbGc..."
      → Serveur extrait le token
      → Serveur décode → {user_id: 1, username: ninon, exp: ...}
      → Serveur vérifie exp → ✅ Pas expiré
      → Serveur cherche ninon dans DB → ✅ Existe
      → Réponse : {id: 1, username: ninon, created_at: "2026-02-15"}
```

**4. Logout**
```
Alice → Clique sur "Déconnexion"
      → localStorage.removeItem("token")
      → Plus de token → Ne peut plus accéder aux routes protégées
```

---

## 🛡️ Sécurité

### Pourquoi c'est sécurisé ?
- ✅ **Mots de passe hashés** : Même si la DB est volée, impossible de lire les passwords
- ✅ **Token signé** : Impossible de modifier le contenu du token sans la clé secrète
- ✅ **Expiration** : Un token volé devient inutile après 30 minutes
- ✅ **Vérification à chaque requête** : Le serveur ne fait jamais confiance au client

### Limites
- ⚠️ **localStorage vulnérable au XSS** : Si un script malveillant s'exécute, il peut voler le token
- ⚠️ **Pas de révocation** : Si un token est volé, il reste valide jusqu'à expiration
- 💡 **Solution avancée** : httpOnly cookies + refresh tokens (hors scope pour l'instant)

---

## 📚 Packages utilisés

- **`passlib[bcrypt]`** : Pour hasher/vérifier les mots de passe
- **`python-jose[cryptography]`** : Pour créer/décoder les JWT
- **`fastapi.security.OAuth2PasswordBearer`** : Pour extraire automatiquement le token du header

---

## ✅ Checklist de compréhension

Tu maîtrises l'authentification JWT si tu peux répondre à ces questions :

- [ ] Pourquoi on ne stocke jamais un mot de passe en clair ?
- [ ] Quelle est la différence entre "hasher" et "chiffrer" ?
- [ ] À quoi sert un token JWT ?
- [ ] Où est stocké le token côté client ?
- [ ] Comment le serveur sait-il qu'un token est valide ?
- [ ] Qu'est-ce qu'une route protégée ?
- [ ] Que se passe-t-il si le token est expiré ?
- [ ] Pourquoi utilise-t-on le header `Authorization` plutôt que le body ?

---

**🎯 Prochaine étape** : Intégrer cette authentification dans `translate_game` ou continuer avec l'Exercice 3 (Leaderboard).
