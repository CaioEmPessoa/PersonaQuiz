const currentQuiz = "/" + window.location.pathname.split("/")[1]
const apiUrl = currentQuiz + "/api"

const queryString = window.location.search;
const urlParams = new URLSearchParams(queryString);
var quiz_id = urlParams.get('id')

const get_questions = function(question_id="1", replace=false){
    fetch(`${apiUrl}/test/`)
    .then( response => {
    fetch(`${apiUrl}/read/${question_id}`).then(response => response.json()).then(
        function(data){
        // se o data retornar um erro, ele mostra o erro.
        if(data["status"] != "Quiz Carregado!"){
            // entrar.style.display = "inline-block"
            return document.getElementById("error").innerHTML = data["status"]

        } 
        else {
            // salva as informações coletadas do quiz do servidor
            let quiz_data = JSON.stringify(data);
            localStorage.setItem('quiz_data', quiz_data);
            const quiz_path = currentQuiz + "/quiz/?id=" + question_id
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
            if (quizID.startsWith(apiUrl)) {
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
if(current_path.indexOf("/quiz/") === -1){
    let startQuizBtn = document.getElementById("startQuiz")
    startQuizBtn.onclick = () => {
        searchBar.focus()
        get_questions(quiz_id, true)
    }
    
    if (quiz_id != null) {
        get_questions(quiz_id, true)
    }
}