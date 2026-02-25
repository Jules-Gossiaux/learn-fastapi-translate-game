 const API_URL = "http://localhost:8000";

// FONCTION 1 : Register
async function register() {
    // Récupérer username et password
    // Envoyer POST /register
    // Afficher message
    const message_element = document.getElementById("reg-message")
    const username = document.getElementById("reg-username").value
    const password = document.getElementById("reg-password").value
    
    const response = await fetch(`${API_URL}/register`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            username: username,
            password: password
        })
    })
    const data = await response.json()
    
    // Vérifier si le register a réussi
    if (!response.ok) {
        message_element.textContent = `Erreur : ${data.detail}`
        return
    }
    
    message_element.textContent = `Le user ${username} est inscrit`
    console.log("Inscription réussie")
}

async function affiche_username() {
    
}

// FONCTION 2 : Login
async function login() {
    // Récupérer username et password
    // Envoyer POST /login
    // Sauvegarder le token dans localStorage
    // Afficher message
    const message_element = document.getElementById("login-message")
    const username = document.getElementById("login-username").value
    const password = document.getElementById("login-password").value
    const response = await fetch(`${API_URL}/login`, {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({
            username: username,
            password: password
        })
    })
    const data = await response.json()
    
    // Vérifier si le login a réussi
    if (!response.ok) {
        message_element.textContent = `Erreur : ${data.detail}`
        return
    }
    
    // Succès : sauvegarder le token et afficher message
    localStorage.setItem("token", data.access_token)
    message_element.textContent = `${username} est connecté`
    console.log("Connexion réussie")
}

// FONCTION 3 : Logout
function logout() {
    localStorage.removeItem('token');   
    console.log("token supprimé")
}

// FONCTION 4 : Get Me (route protégée)
async function getMe() {
    // Récupérer le token depuis localStorage
    // Envoyer GET /me avec Header Authorization
    // Afficher les infos
    
    const infos_on_me = document.getElementById("protected-message")
    const token = localStorage.getItem("token")
    const response = await fetch(`${API_URL}/me`, {
        method: "GET",
        headers: {'Authorization': `Bearer ${token}`}
    })
    const data = await response.json()
    if (!response.ok) {
        infos_on_me.textContent = `Erreur : ${data.detail}`
        return
    }
    infos_on_me.textContent = `id: ${data.id}, username: ${data.username}, created_at: ${data.created_at}`

}

// FONCTION 5 : Test route protégée
async function testProtected() {
    // Récupérer le token depuis localStorage
    // Envoyer GET /protected avec Header Authorization
    // Afficher le message
    const message_zone = document.getElementById("protected-message")

    const token = localStorage.getItem("token")

    const response = await fetch(`${API_URL}/protected`, {
        method: "GET",
        headers: {"Authorization": `Bearer ${token}`}
    })
    const data = await response.json()
    if (!response.ok) {
        message_zone.textContent = `Erreur : ${data.detail}`
        return
    }
    message_zone.textContent = data.message
}