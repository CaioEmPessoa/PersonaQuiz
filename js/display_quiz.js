// Quiz Generation

// read data
var data = localStorage['quiz_data'];
if (data==undefined) {
    
    const queryString = window.location.search;
    const urlParams = new URLSearchParams(queryString);
    const quiz_id = urlParams.get('id')
    
    window.location.href = "/UserQuizMaker/view/read_quiz.html?id=" + quiz_id
}

data = JSON.parse(data)
localStorage.removeItem('quiz_data');

if (user_progress==undefined) {
    var user_progress = {
        "right":0,
        "wrong":0,
        "qstn_number":1,
    }
}

// creating the numbers paragraphs
// creating the numbers array
const qstn_numb_array = Array.from({length: data["qstn_count"]}, (_, i) => i + 1)

// loop trouht the numbers array
for(let value of qstn_numb_array){

    const para = document.createElement("p")
    const text = document.createTextNode(value)
    para.setAttribute("id", "num-box-"+value)
    para.appendChild(text)
    
    const numbers_div = document.getElementById("numbers")
    numbers_div.appendChild(para)
    
    // se o numero for maior que 6, cria o elemento com display none
    if (value >= 6){
        let num_box = document.getElementById("num-box-"+value)
        num_box.style.display = "none"
    }
}

// creates 
if (data["qstn_count"] >= 6) {
    const para = document.createElement("p");
    const text = document.createTextNode("...");
    para.setAttribute("id", "continue")
    para.appendChild(text);
    const numbers_div = document.getElementById("continue");
    numbers_div.appendChild(para);
}

const move_numbers = function() {
    var qstn_number = user_progress["qstn_number"]

    if (qstn_number >= 6){
        for(let value of qstn_numb_array){
            if (value >= qstn_number+1){
                let num_box = document.getElementById("num-box-"+value)
                num_box.style.display = "none"
            } 
            else if (value <= qstn_number-5){
                let num_box = document.getElementById("num-box-"+value)
                num_box.style.display = "none"
            } 
            else {
                let num_box = document.getElementById("num-box-"+value)
                num_box.style.display = "inline-block"
            }
        }
    }
}


let answers_div = document.getElementById("perguntas")

// display data
const refresh_qstn = function(){
    var qstn_number = user_progress["qstn_number"]
    var qstn_count = data["qstn_count"]

    if (qstn_number == qstn_count+1){
        // hide the answers
        answers_div.style.display = "none"

        document.getElementById("title").innerHTML = "Parabens! <br> Você acertou " + user_progress["right"] + " de " + qstn_count + " perguntas!"
            

    } else {
        document.getElementById("title").innerHTML = data["Question " + qstn_number]["question"]

        document.getElementById("1").innerHTML = data["Question " + qstn_number]["options"][0]
        document.getElementById("2").innerHTML = data["Question " + qstn_number]["options"][1]
        document.getElementById("3").innerHTML = data["Question " + qstn_number]["options"][2]
        document.getElementById("4").innerHTML = data["Question " + qstn_number]["options"][3]
    }
    if (qstn_number <= qstn_count-1){
        move_numbers()
    } else  {
        let continue_p = document.getElementById("continue")
        let last_numb = document.getElementById("num-box-" + String(qstn_count))
        continue_p.style.display = "none"
        last_numb.style.display = "inline-block"
    }
}
refresh_qstn()

const check_answr = function(answer){
    let given_answer = String(answer.innerHTML)
    let button_pressed = document.getElementById(answer.id)
    let num_box = document.getElementById("num-box-"+ user_progress["qstn_number"])
    let right_answer = String(data["Question " + user_progress["qstn_number"]]["answer"])
    
    button_pressed.classList.remove("reset_answr")
    // caso a resposta esteja correta...
    if (given_answer == right_answer){
        
        button_pressed.classList.add("right_answr")
        num_box.classList.add("right_answr")
        
        // adds a point to the right questions
        user_progress["right"] = user_progress["right"] += 1
        
    } 
    
    // caso a resposta esteja errada...
    else {
        button_pressed.classList.add("wrong_answr")
        num_box.classList.add("wrong_answr")

        for (let i = 1; i<=4; i++) {
            var resposta = document.getElementById(i);
            if (resposta.innerHTML == right_answer){
                resposta.classList.add("right_answr");
            }    
        }
        
        // adds a point to the wrong questions
        user_progress["wrong"] = user_progress["wrong"] += 1
        
    }

    user_progress["qstn_number"] += 1
    // resets and prepares the quiz to the next question
    setTimeout(() => {
        
        for (let i = 1; i<=4; i++) {
            var resposta = document.getElementById(i);
            resposta.classList.remove("right_answr")
            resposta.classList.remove("wrong_answr")
            resposta.classList.add("reset_answr")
        }

        refresh_qstn()
    }, 1000);
    
}

// END Quiz Generation


