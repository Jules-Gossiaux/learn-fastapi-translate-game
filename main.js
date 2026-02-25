// L'adresse de ton backend
const API_URL = "http://localhost:8000";

// Éléments html
const selectLevel = document.getElementById("difficulty-level")
const englishWordZone = document.getElementById("english-word")
const responseInput = document.getElementById("user-traduction")
const correctionZone = document.getElementById("correction-zone")
const historicalAccordion = document.getElementById("historical-accordion")
const historicalZone = document.getElementById("historical")
const statisticsAccordion = document.getElementById("statistics-accordion")
const scoreMessage = document.getElementById("score")
const attemptsMessage = document.getElementById("attempts")
const verifyButton = document.getElementById("verify-button")
const newWordButton = document.getElementById("new-word-button")
const leaderboardAccordion = document.getElementById("leaderboard-accordion")
const tbody = document.getElementById("statistics")
const totalZone = document.getElementById("statistics-total")
const selectLevelLeaderboard = document.getElementById("leaderboard-filter")

async function register() {
    const username = document.getElementById("reg-username").value
    const pwd = document.getElementById("reg-password").value
    const message_zone = document.getElementById("reg-message")
    if (username === "" || pwd === ""){
        console.log(username, pwd)
        message_zone.textContent = "Le username et le password doivent être remplis"
    }
    else{
        console.log("les username et le pwd sont complets")
        console.log(username, pwd);
        const response = await fetch(`${API_URL}/users`, {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({
                username: username,
                password: pwd
            })
        })
        const data = await response.json()
        console.log(data)

        if (!response.ok){
            message_zone.textContent = data["detail"]
        }

        else {
            message_zone.textContent = data["message"]
        }
    }
}

async function login() {
    const username = document.getElementById("login-username").value
    const pwd = document.getElementById("login-password").value
    const messageZoneId = "login-message"
    
        
    const response = await fetch(`${API_URL}/auth/login`, {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({
            username: username,
            password: pwd
        })
    })
    const data = await response.json()
    console.log(data)
    if (!response.ok){
        document.getElementById(messageZoneId).textContent = data["detail"]
    }
    else {
        console.log("Token:", data.token)
        localStorage.setItem("token", data.token)
        localStorage.setItem("username", data.username)
        localStorage.setItem("user_id", data.user_id)
        localStorage.setItem("level", data.level)
        init()
    }

}

async function logout() {
    if (localStorage.getItem("username")) {
        console.log("déconnecté")
        localStorage.removeItem("token")
        localStorage.removeItem("username")
        localStorage.removeItem("user_id")
        localStorage.removeItem("level")
        window.location.reload();
    }
    else {return}
}


// quand le level change, fonction
async function changeLevel() {
    const level = selectLevel.value
    const user_id = localStorage.getItem("user_id")
    const token = localStorage.getItem("token")
    if (user_id === null) { console.log("le user n'est pas connecté ou l'id n'est pas bon"); return}
    else {
        const response = await fetch(`${API_URL}/users/${user_id}/level`, {
            method: "PATCH",
            headers: {"Content-Type": "application/json", "Authorization": `Bearer ${token}`},
            body: JSON.stringify({
                level: level,
            })
        })
        const data = await response.json()
        console.log(data.message)
        localStorage.setItem("level", level)
    }
}


let current_word = null
async function newWord() {
    const level = localStorage.getItem("level")
    try {
        const response = await fetch(`${API_URL}/words/english/${level}`)
        if (!response.ok) {
            const error = await response.json()
            englishWordZone.textContent = "Erreur : " + error.detail
            englishWordZone.style.color = "red"
            return
        }
        const data = await response.json()
        if (data != null) {
            current_word = data
            englishWordZone.textContent = data.english_traduction
            englishWordZone.style.color = "#2196F3";
            responseInput.disabled = false;
            responseInput.focus();
            responseInput.value = "";
            correctionZone.textContent = "";
            verifyButton.disabled = false;
        }
    }
    catch(error) {
        englishWordZone.textContent = "Serveur inaccessible, réessaie plus tard"
        englishWordZone.style.color = "red"
    }
}


async function verify(){
    const userResponse = responseInput.value
    const userAnswer = userResponse.trim().toLowerCase();
    console.log(typeof userAnswer);
    const correctAnswer = current_word.french_traduction.trim().toLowerCase();

    if (userAnswer === correctAnswer) {
        englishWordZone.style.color = "green";
        const guess = {
            user_id: localStorage.getItem("user_id"),
            word_id: current_word.id,
            guess: userAnswer,
            is_correct: true,
            date: new Date().toISOString()
        }   
        await addGuess(guess)
    } else {
        correctionZone.textContent = ("correction: " + current_word.french_traduction);
        correctionZone.style.color = "black"
        englishWordZone.style.color = "red";
        const guess = {
            user_id: localStorage.getItem("user_id"),
            word_id: current_word.id,
            guess: userAnswer,
            is_correct: false,
            date: new Date().toISOString()
        }   
        await addGuess(guess)

    }
    updateScoreDisplay()
}


async function addGuess(guess) {
    console.log(guess)

    try {
        const response = await fetch(`${API_URL}/guesses`, {
        method: "POST",
        headers: {
            "Authorization": `Bearer ${localStorage.getItem("token")}`,
            "Content-Type": "application/json"
        },
        body: JSON.stringify(guess)
    })
    if (!response.ok) {
        const error = await response.json()
        console.error("Erreur enregistrement tentative:", error.detail)
    }
    }
    catch (error){
        console.log("error", error)
    }
}

async function getGuesses() {
    const user_id = localStorage.getItem("user_id")
    const token = localStorage.getItem("token")
    const response = await fetch(`${API_URL}/guesses/${user_id}`, {
        method: "GET",
        headers: {"Authorization": `Bearer ${token}`}
    })
    const data = await response.json()

    if (!data || data.length === 0) {
        historicalZone.innerHTML = "<p style='color:#888; font-style:italic;'>Aucune tentative pour le moment.</p>"
        return
    }

    let html = ""
    data.forEach(item => {
        const isCorrect = item.guess.trim().toLowerCase() === item.french_traduction.trim().toLowerCase()
        const date = new Date(item.date).toLocaleString("fr-FR", {dateStyle: "short", timeStyle: "short"})

        const bgColor = isCorrect ? "#d4edda" : "#f8d7da"
        const borderColor = isCorrect ? "#28a745" : "#dc3545"
        const icon = isCorrect ? "✅" : "❌"

        const correctionHtml = isCorrect
            ? ""
            : `<span style="color:#dc3545;"> → <strong>${item.french_traduction}</strong></span>`

        html += `
        <div style="
            background: ${bgColor};
            border-left: 4px solid ${borderColor};
            border-radius: 5px;
            padding: 8px 12px;
            margin-bottom: 6px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            font-size: 14px;
        ">
            <span>
                ${icon}
                <strong>${item.english_traduction}</strong>
                → <em>${item.guess}</em>${correctionHtml}
            </span>
            <span style="color:#888; font-size:12px;">${date}</span>
        </div>`
    })

    historicalZone.innerHTML = html
}

async function updateScoreDisplay() {
    const user_id = localStorage.getItem("user_id")
    const token = localStorage.getItem("token")
    const response = await fetch(`${API_URL}/statistics/${user_id}`, {
        method: "GET",
        headers: {"Authorization": `Bearer ${token}`}
    })
    const data = await response.json()
    scoreMessage.textContent = data.correct
    attemptsMessage.textContent = data.total
}

async function resetScore() {
    const user_id = localStorage.getItem("user_id")
    const token = localStorage.getItem("token")
    const response = await fetch(`${API_URL}/users/${user_id}/reset`, {
        method: "DELETE",
        headers: {"Authorization": `Bearer ${token}`}
    })
    updateScoreDisplay()
}


async function leaderboard() {
    const level = selectLevelLeaderboard.value

    const response = await fetch(`${API_URL}/leaderboard?level=${level}`)
    const data = await response.json()
    
    const tbody = document.getElementById("leaderboard-body")
    const currentUsername = localStorage.getItem("username")
    
    tbody.innerHTML = ""
    
    data.forEach((user, index) => {
        const row = document.createElement("tr")
        
        if (user.username === currentUsername) {
            row.classList.add("current-user")
        }
        
        const rank = index + 1
        const rankClass = rank <= 3 ? `rank-${rank}` : ""
        
        row.innerHTML = `
            <td class="${rankClass}">${rank}</td>
            <td>${user.username}</td>
            <td>${user.score}</td>
            <td>${user.attempts}</td>
        `
        tbody.appendChild(row)
})
}

async function statisticsTable() {
    const user_id = localStorage.getItem("user_id")
    const token = localStorage.getItem("token")
    const response = await fetch(`${API_URL}/statistics/${user_id}/table`, {
        method: "GET",
        headers: {"Authorization": `Bearer ${token}`}
    })
    const data = await response.json()

    
    if (data.length === 0) {
        tbody.innerHTML = "<tr><td colspan='4'>Vous n'avez pas encore joué</td></tr>"
        return
    }
    
    tbody.innerHTML = ""
    
    let totalTentatives = 0
    let totalCorrectes = 0
    const ordre = ["facile", "moyen", "difficile"]
    const dataTrie = ordre.map(level => data.find(row => row.level === level) || { level, total: 0, correct: 0 })
    dataTrie.forEach((row) => {
        const taux = row.total === 0 ? "N/A" : ((row.correct / row.total) * 100).toFixed(1) + "%"
        totalTentatives += row.total
        totalCorrectes += row.correct
        
        const tr = document.createElement("tr")
        tr.innerHTML = `
            <td>${row.level}</td>
            <td>${row.total}</td>
            <td>${row.correct}</td>
            <td>${taux}</td>
        `
        tbody.appendChild(tr)
    })
    
    totalZone.textContent = `Total : ${totalTentatives} tentatives, ${totalCorrectes} correctes`
}

async function init() {
    // récupère le user et met à jour tout ce qui est en rapport
    const username = localStorage.getItem("username");
    const token = localStorage.getItem("token")
    const selectLevel = document.getElementById("difficulty-level")
    const loginMessage = document.getElementById("login-message")

    if (username === null) {document.getElementById("login-message").textContent = "Aucun user connecté"; return}
    if (!token) {
        console.log("Pas de token, connecte-toi !");
        return;
    }
    else{
        const response = await fetch(`${API_URL}/users/${username}`, {
            method:"GET",
            headers: {"Authorization": `Bearer ${token}`}
        })
        const data = await response.json()
        console.log(data);
        
        // Modifie le select sur le bon niveau
        selectLevel.value = data.level
        // Modifie l'affichage du pseudo
        loginMessage.textContent = `${data.username} est connecté`
        verifyButton.disabled = false;
        newWordButton.disabled = false;
        updateScoreDisplay()
        leaderboard()
    }
}


// Section des écouteurs d'évènements
selectLevel.addEventListener("change", changeLevel)

historicalAccordion.addEventListener("toggle", async () => {
    if (historicalAccordion.open) {
        getGuesses()
    }
});

statisticsAccordion.addEventListener("toggle", async () => {
    if (statisticsAccordion.open) {
        statisticsTable()
    }
})

leaderboardAccordion.addEventListener("toggle", async () => {
    if (leaderboardAccordion.open) {
        leaderboard()
    }
})

selectLevelLeaderboard.addEventListener("change", leaderboard)

window.addEventListener('load', () => {
    init()
});
