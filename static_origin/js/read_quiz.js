const DEBUG = true

if (DEBUG == true) {
  var API_URL = "http://127.0.0.1:8000/SteamQuiz/api"
  var MAIN_URL = "http://127.0.0.1:8000/SteamQuiz/"
} else if (DEBUG == false) {
    var API_URL = "https://personaquiz.onrender.com/SteamQuiz/api"
    var MAIN_URL = "https://personaquiz.onrender.com/SteamQuiz"
}

const queryString = window.location.search;
const urlParams = new URLSearchParams(queryString);
var quiz_id = urlParams.get('id')

const get_questions = function(question_id="1", replace=false){
    fetch(`${API_URL}/test/`)
    .then( response => {
    fetch(`${API_URL}/read/${question_id}`).then(response => response.json()).then(
        function(data){
        // se o data retornar um erro, ele mostra o erro.
        if(data["status"] != "Quiz Carregado!"){
            entrar.style.display = "inline-block"
            return document.getElementById("error").innerHTML = data["status"]

        } 
        else {
            // salva as informações coletadas do quiz do servidor
            let quiz_data = JSON.stringify(data);
            localStorage.setItem('quiz_data', quiz_data);
            const quiz_path = "/SteamQuiz/quiz/?id=" + question_id
            if (replace) {
                window.location.replace(quiz_path)
                return
            } else {
                return window.location = quiz_path
            }
        }
    });
    })
    .catch(error => {
        let error_label = document.getElementById("error") 
        return error_label.innerHTML = "Erro do servidor, tente novamente mais tarde."
    })
}

// SEARCH BAR BEHAVIOUR
let searchBar = document.getElementById("searchBar")
searchBar.addEventListener("keydown", function(event) {
    if (event.key === "Enter") {
        if (searchBar === document.activeElement) {
            let quizID = searchBar.value

            // checking if is a url in the search bar or an id
            if (quizID.startsWith(API_URL)) {
                get_questions(quizID.slice(-6))
            }
            else if (quizID.length == 6) {
                get_questions(quizID)
            } 
            else {
                // TODO: TRIGGER ERROR POPUP
                return
            }
        }
    }
})

// INDEX PAGE SCRIPTS
let current_path = window.location.pathname
if(current_path == "/SteamQuiz/"){
    let startQuizBtn = document.getElementById("startQuiz")
    startQuizBtn.onclick = () => {
        searchBar.focus()
    }
    
    if (quiz_id != null) {
        get_questions(quiz_id, true)
    }
}