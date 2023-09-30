const queryString = window.location.search;
const urlParams = new URLSearchParams(queryString);
const quiz_id = urlParams.get('id')

console.log(quiz_id)

// Get quiz already made <--------------------------------<

const request = function(request_id="1"){
    fetch('http://127.0.0.1:5000/steam_app/test')
    .then( response => {
    fetch("http://127.0.0.1:5000/steam_app/open_created/" + request_id).then(response => response.json()).then(
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
            const quiz_path = "/view/quiz.html?id=" + request_id
            return window.location.href = quiz_path
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