# 🎯 EXERCICE 1 : Gestion Multi-Joueurs

## 📚 PARTIE 1 : THÉORIE - Concepts nouveaux

### 1️⃣ Variables de session / Gestion d'état côté serveur

#### C'est quoi ?
Une **variable de session** permet de garder des informations **entre plusieurs requêtes** pour un utilisateur donné.

**Problème sans session :**
```
Requête 1 : User choisit "Joueur 1"
Requête 2 : Serveur ne sait plus quel joueur était choisi ❌
```

**Solution avec session :**
```
Requête 1 : User choisit "Joueur 1" → Serveur garde en mémoire
Requête 2 : Serveur se souvient que c'est "Joueur 1" ✅
```

#### En Python (approche simple)
Pour cet exercice, on va utiliser une **variable globale** côté serveur :

```python
# Variable globale qui garde le joueur actif
joueur_actif_id = 1  # Par défaut, joueur 1
```

**Comment ça marche :**
- Quand le serveur démarre → `joueur_actif_id = 1`
- User change pour joueur 2 → `joueur_actif_id = 2`
- Toutes les autres routes utilisent `joueur_actif_id` pour savoir avec quel joueur travailler

**Exemple concret :**
```python
joueur_actif_id = 1  # Variable globale

@app.get("/score")
def get_score():
    # Cette route sait automatiquement quel joueur utiliser !
    joueur = get_joueur(joueur_actif_id)
    return {"score": joueur["score"]}
```

#### ⚠️ Limites de cette approche
- Si plusieurs personnes utilisent l'app en même temps → ils partagent le même joueur actif
- Plus tard, tu apprendras les **vraies sessions** (cookies, JWT) pour gérer chaque utilisateur séparément

#### 💡 Pourquoi cette approche quand même ?
- Simple à comprendre
- Parfait pour apprendre le concept
- Fonctionne bien pour une utilisation locale (un seul utilisateur)

---

### 2️⃣ Dropdown (sélecteur) en HTML/JavaScript

#### C'est quoi ?
Un **dropdown** (menu déroulant) permet de choisir parmi plusieurs options.

#### HTML : `<select>` et `<option>`

**Structure de base :**
```html
<select id="monSelecteur">
    <option value="1">Option 1</option>
    <option value="2">Option 2</option>
    <option value="3">Option 3</option>
</select>
```

**Ce que ça affiche :**
```
[Choisir ▼]
  Option 1
  Option 2
  Option 3
```

**Attributs importants :**
- `id` : Pour récupérer l'élément en JavaScript
- `value` : La valeur envoyée (ce qui compte pour le code)
- Texte entre les balises : Ce que l'utilisateur voit

**Exemple pour notre jeu :**
```html
<select id="selecteurJoueur">
    <option value="1">Joueur 1</option>
    <option value="2">Joueur 2</option>
    <option value="3">Joueur 3</option>
</select>
```

#### JavaScript : Récupérer la valeur sélectionnée

**Méthode 1 : Quand on veut la valeur maintenant**
```javascript
const selecteur = document.getElementById("selecteurJoueur");
const valeurChoisie = selecteur.value;  // "1", "2" ou "3"
console.log(valeurChoisie);  // Affiche la valeur
```

**Méthode 2 : Détecter quand la sélection change**
```javascript
const selecteur = document.getElementById("selecteurJoueur");

selecteur.addEventListener("change", function() {
    const valeurChoisie = selecteur.value;
    console.log("Joueur choisi :", valeurChoisie);
    // Ici tu peux appeler une fonction pour changer le joueur actif
});
```

#### JavaScript : Créer les options dynamiquement

**Si tu as une liste de joueurs depuis l'API :**
```javascript
// Liste reçue depuis GET /joueurs
const joueurs = [
    {id: 1, pseudo: "Alice"},
    {id: 2, pseudo: "Bob"},
    {id: 3, pseudo: "Charlie"}
];

const selecteur = document.getElementById("selecteurJoueur");

// Vider le selecteur d'abord
selecteur.innerHTML = "";

// Créer une option pour chaque joueur
joueurs.forEach(joueur => {
    const option = document.createElement("option");
    option.value = joueur.id;  // La valeur (ce qui compte)
    option.textContent = joueur.pseudo;  // Le texte affiché
    selecteur.appendChild(option);
});
```

**Résultat :**
```html
<select id="selecteurJoueur">
    <option value="1">Alice</option>
    <option value="2">Bob</option>
    <option value="3">Charlie</option>
</select>
```

---

### 3️⃣ Gestion d'état : Synchroniser Frontend et Backend

#### Le problème
Ton frontend doit savoir **quel joueur est actif** pour l'afficher à l'utilisateur.

**Exemple :**
```
Backend : joueur_actif_id = 2
Frontend : Doit afficher "Bob est connecté"
```

#### Deux approches

**Approche 1 : Frontend garde l'info localement**
```javascript
// Variable JavaScript globale
let joueurActif = {id: 1, pseudo: "Alice"};

// Afficher
document.getElementById("nomJoueur").textContent = joueurActif.pseudo;
```

**Approche 2 : Frontend demande au backend**
```javascript
async function afficherJoueurActif() {
    const response = await fetch("http://localhost:8000/joueur-actif");
    const joueur = await response.json();
    document.getElementById("nomJoueur").textContent = joueur.pseudo;
}
```

#### 💡 Quelle approche choisir ?

**Pour cet exercice : Approche 1 (plus simple)**
- Moins de requêtes HTTP
- Plus rapide
- Suffisant pour apprendre

**Plus tard : Approche 2 (plus robuste)**
- Source de vérité = backend
- Synchronisation garantie
- Meilleur pour production

---

### 4️⃣ Cycle complet : Changer de joueur

**Étapes quand l'utilisateur change de joueur :**

1. **Frontend** : User clique sur dropdown et choisit "Bob"
2. **Frontend** : JavaScript détecte le `change` event
3. **Frontend** : Envoie `POST /joueurs/actif` avec `{joueur_id: 2}`
4. **Backend** : Reçoit la requête
5. **Backend** : Change `joueur_actif_id = 2` (variable globale)
6. **Backend** : Répond `{success: true}`
7. **Frontend** : Reçoit la confirmation
8. **Frontend** : Met à jour l'affichage "Bob est connecté"

**Schéma :**
```
User → Dropdown → JavaScript → POST /joueurs/actif → Backend change variable
                                                    ↓
Frontend ← Répond OK ← Backend
```

---

## 💡 PARTIE 2 : CE QUE TU DOIS CODER

### 📁 Dans `database.py`

**Fonctions à créer :**

1. **`creer_joueur(pseudo)`**
   - Rôle : Insérer un nouveau joueur dans la table `joueurs`
   - Paramètres : `pseudo` (str)
   - Retourne : L'ID du nouveau joueur créé
   - SQL : `INSERT INTO joueurs ...`

2. **`get_tous_les_joueurs()`**
   - Rôle : Récupérer la liste de TOUS les joueurs
   - Paramètres : Aucun
   - Retourne : Liste de dictionnaires `[{id, pseudo, score, tentatives}, ...]`
   - SQL : `SELECT * FROM joueurs`

3. **Modifier `init_db()` ?**
   - Question à te poser : Est-ce que la table `joueurs` existe déjà ?
   - Si OUI → Rien à faire ✅
   - Si NON → Créer la table avec colonnes `id, pseudo, score, tentatives`

**💭 Réflexion :**
- Regarde ton fichier `database.py` actuel
- Est-ce que `get_joueur(joueur_id)` existe déjà ? (Oui !)
- Est-ce que la table `joueurs` existe ? (Vérifie `init_db()`)
- Qu'est-ce qui manque pour gérer plusieurs joueurs ?

---

### 📁 Dans `main.py`

**Variable globale à ajouter (en haut du fichier) :**
```python
# Garde le joueur actuellement actif
joueur_actif_id = 1  # Par défaut : joueur 1
```

**Routes à créer :**

1. **`POST /joueurs`**
   - Rôle : Créer un nouveau joueur
   - Body : `{pseudo: "Alice"}`
   - Appelle : `creer_joueur(pseudo)` de database.py
   - Retourne : `{id: 1, pseudo: "Alice"}`
   - Pydantic model : À créer (juste le pseudo)

2. **`GET /joueurs`**
   - Rôle : Récupérer tous les joueurs
   - Paramètres : Aucun
   - Appelle : `get_tous_les_joueurs()` de database.py
   - Retourne : `[{id: 1, pseudo: "Alice", score: 10}, ...]`

3. **`POST /joueurs/actif`**
   - Rôle : Changer le joueur actif
   - Body : `{joueur_id: 2}`
   - Action : Change la variable globale `joueur_actif_id`
   - Retourne : `{success: true, joueur_id: 2}`
   - Pydantic model : À créer (juste joueur_id)
   - ⚠️ Utilise `global joueur_actif_id` dans la fonction !

4. **BONUS : `GET /joueur-actif` (optionnel)**
   - Rôle : Récupérer les infos du joueur actif
   - Appelle : `get_joueur(joueur_actif_id)`
   - Retourne : `{id: 1, pseudo: "Alice", score: 10, ...}`

**💭 Réflexion :**
- Comment utiliser la variable globale dans une fonction ? (mot-clé `global`)
- Quelles routes existantes doivent maintenant utiliser `joueur_actif_id` ?

**Routes à MODIFIER :**
- Toutes les routes qui utilisent actuellement un `joueur_id` fixe (ex: `joueur_id=1`)
- Remplace par `joueur_actif_id` (la variable globale)
- Exemples : `/score`, `/verifier`, `/reset`, etc.

---

### 📁 Dans `index.html`

**Éléments HTML à ajouter :**

1. **Dropdown pour choisir le joueur**
   - Tag : `<select id="selecteurJoueur">`
   - Emplacement : En haut de la page, bien visible
   - Contenu : Les `<option>` seront créées dynamiquement en JavaScript

2. **Affichage du joueur actif**
   - Exemple : `<p>Joueur : <span id="nomJoueur">...</span></p>`
   - Mise à jour quand on change de joueur

3. **Formulaire pour créer un nouveau joueur (optionnel)**
   - Input pour le pseudo
   - Bouton "Créer joueur"

**Fonctions JavaScript à créer :**

1. **`chargerJoueurs()`**
   - Rôle : Récupérer tous les joueurs depuis `GET /joueurs`
   - Action : Remplir le dropdown avec les options
   - Quand : Au chargement de la page

2. **`changerJoueurActif(joueurId)`**
   - Rôle : Envoyer `POST /joueurs/actif` avec le nouveau joueur_id
   - Action : Mettre à jour l'affichage du nom
   - Quand : Quand le user change le dropdown

3. **`creerNouveauJoueur(pseudo)` (optionnel)**
   - Rôle : Envoyer `POST /joueurs` avec le pseudo
   - Action : Recharger la liste des joueurs
   - Quand : Bouton "Créer joueur" cliqué

**Modifications JavaScript nécessaires :**

- **Au chargement de la page :**
  - Appeler `chargerJoueurs()`
  
- **Event listener sur le dropdown :**
  - Détecter `change`
  - Appeler `changerJoueurActif()`

**💭 Réflexion :**
- Où placer le dropdown dans le HTML ? (En haut, dans une section dédiée ?)
- Comment garder le score à jour quand on change de joueur ?

---

## 🎯 PARTIE 3 : ORDRE DE TRAVAIL RECOMMANDÉ

### Étape 1 : Backend (Database)
1. Ouvre `translate_game/database.py`
2. Vérifie si la table `joueurs` existe dans `init_db()`
3. Code `creer_joueur(pseudo)`
4. Code `get_tous_les_joueurs()`
5. **Test** : Utilise `test_database.py` ou crée un fichier de test temporaire

### Étape 2 : Backend (API)
1. Ouvre `translate_game/main.py`
2. Ajoute la variable globale `joueur_actif_id = 1` en haut
3. Crée les modèles Pydantic nécessaires
4. Code la route `POST /joueurs`
5. Code la route `GET /joueurs`
6. Code la route `POST /joueurs/actif` (attention au mot-clé `global` !)
7. Modifie les routes existantes pour utiliser `joueur_actif_id`
8. **Test** : Va sur `http://localhost:8000/docs` et teste chaque route

### Étape 3 : Frontend
1. Ouvre `translate_game/index.html`
2. Ajoute le HTML du selecteur
3. Code `chargerJoueurs()` en JavaScript
4. Code `changerJoueurActif(joueurId)`
5. Ajoute les event listeners
6. Appelle `chargerJoueurs()` au chargement de la page
7. **Test** : Ouvre dans le navigateur et vérifie que tout marche

### Étape 4 : Test complet
1. Démarre le serveur : `uvicorn main:app --reload`
2. Ouvre `index.html`
3. Crée quelques joueurs (si tu as fait le formulaire)
4. Change de joueur avec le dropdown
5. Joue au jeu avec différents joueurs
6. Vérifie que chaque joueur a son propre score

---

## 🆘 AIDE-MÉMOIRE

### Mot-clé `global` en Python
```python
joueur_actif_id = 1  # Variable globale

def changer_joueur(nouveau_id):
    global joueur_actif_id  # OBLIGATOIRE pour modifier une variable globale
    joueur_actif_id = nouveau_id
```

### Créer des options dynamiquement
```javascript
joueurs.forEach(joueur => {
    const option = document.createElement("option");
    option.value = joueur.id;
    option.textContent = joueur.pseudo;
    selecteur.appendChild(option);
});
```

### Event listener sur select
```javascript
selecteur.addEventListener("change", function() {
    const id = selecteur.value;
    // Faire quelque chose avec id
});
```

### fetch POST avec body
```javascript
fetch("http://localhost:8000/joueurs/actif", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({joueur_id: 2})
});
```

---

## ✅ Checklist finale

Avant de dire que c'est terminé, vérifie :

- [ ] Je peux créer un nouveau joueur
- [ ] Je peux voir la liste de tous les joueurs dans le dropdown
- [ ] Quand je change de joueur, l'affichage se met à jour
- [ ] Chaque joueur a son propre score
- [ ] Si je joue avec joueur 1, puis je passe à joueur 2, les scores sont différents
- [ ] Le serveur se souvient du joueur actif entre les requêtes

---

## 💪 Conseils

1. **Code une petite partie à la fois**
   - Ne fais pas tout d'un coup
   - Teste après chaque fonction

2. **Utilise `console.log()` et `print()`**
   - Frontend : `console.log("Joueur choisi:", id);`
   - Backend : `print(f"Joueur actif changé: {joueur_actif_id}")`

3. **Teste sur `/docs` d'abord**
   - Avant de coder le frontend
   - Vérifie que les routes marchent

4. **N'hésite pas à demander de l'aide**
   - Si tu bloques sur un concept
   - Si tu as une erreur que tu ne comprends pas

---

**Prêt à coder ? 🚀**

Commence par l'étape 1 (Backend - Database) et dis-moi quand tu veux que je vérifie ton code !
