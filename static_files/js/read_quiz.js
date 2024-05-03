const DEBUG = false

if (DEBUG == true) {
  var API_URL = "http://127.0.0.1:8000/SteamQuiz/api"
} else if (DEBUG == false) {
  var API_URL = "render_link" // TODO: GET RENDER LINK
}

const queryString = window.location.search;
const urlParams = new URLSearchParams(queryString);
const quiz_id = urlParams.get('id')

console.log(quiz_id)

// Get quiz already made <--------------------------------<

const request = function(request_id="1"){
    fetch(`${API_URL}/test/`)
    .then( response => {
    fetch(`${API_URL}/read/${request_id}`).then(response => response.json()).then(
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
            const quiz_path = "/SteamQuiz/quiz/?id=" + request_id
            return window.location = quiz_path
        }
    });
    })
    .catch(error => {
        let error_label = document.getElementById("error") 
        return error_label.innerHTML = "Erro do servidor, tente novamente mais tarde."
    })
}

if(quiz_id){
    request(quiz_id)
}

let entrar = document.getElementById("entrar-criado")
entrar.onclick = function(){
    let quizID = document.getElementById("quiz-id").value
    request(quizID)
}

// END Get quiz >-------------------------------->