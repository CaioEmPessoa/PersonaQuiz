// Quiz Generation

// read data
var data = localStorage['quiz_data'];
if (data==undefined) {
    console.log("Sem data.")
    
    const queryString = window.location.search;
    const urlParams = new URLSearchParams(queryString);
    const quiz_id = urlParams.get('id')
    
    window.location.href = "/view/read_quiz.html?id=" + quiz_id
}

data = JSON.parse(data)
localStorage.removeItem('quiz_data');

if (user_progress==undefined) {
    console.log("Sem Progresso.")
    var user_progress = {
        "right":0,
        "wrong":0,
        "qstn_number":1,
    }
}
console.log(user_progress)

// creating the numbers paragraphs
// creating the numbers array
const qstn_numb = Array.from({length: data["qstn_count"]}, (_, i) => i + 1)

// loop trouht the numbers array
for(let value of qstn_numb){
    console.log(value)
    console.log(user_progress["qstn_number"])

    const para = document.createElement("p")
    const text = document.createTextNode(value)
    para.setAttribute("id", "num-box-"+value)
    para.appendChild(text)
    
    const numbers_div = document.getElementById("numbers")
    numbers_div.appendChild(para)
    
    if (value >= 6){
        let num_box = document.getElementById("num-box-"+value)
        num_box.style.display = "none"
    } else if (value >= user_progress["qstn_number"]+4) {
        const para = document.createElement("p");
        const text = document.createTextNode("...");
        para.setAttribute("id", "continue")
        para.appendChild(text);
        const numbers_div = document.getElementById("continue");
        numbers_div.appendChild(para);
    } 
}

const move_numbers = function() {
    if (user_progress["qstn_number"] >= 5){
        for(let value of qstn_numb){
            if (value >= user_progress["qstn_number"]+1){
                let num_box = document.getElementById("num-box-"+value)
                num_box.style.display = "none"
            } 
            else if (value <= user_progress["qstn_number"]-5){
                let num_box = document.getElementById("num-box-"+value)
                num_box.style.display = "none"
            } 
            else {
                let num_box = document.getElementById("num-box-"+value)
                num_box.style.display = "inline-block"
            }
        }
    }

    if (user_progress["qstn_number"] == data["qstn_count"]){
        let continue_p = document.getElementById("continue")
        continue_p.style.display = "none"
    }
}


let answers_div = document.getElementById("perguntas")

// display data
let load_qstn = function(){
    
    if (user_progress["qstn_number"] == data["qstn_count"]+1){
        // hide the answers
        console.log(answers_div)
        answers_div.style.display = "none"

        document.getElementById("title").innerHTML = "Parabens! <br> Você acertou " + user_progress["right"] + " de " + data["qstn_count"] + " perguntas!"
            

    } else {
        document.getElementById("title").innerHTML = data["Question " + user_progress["qstn_number"]]["question"]

        document.getElementById("1").innerHTML = data["Question " + user_progress["qstn_number"]]["options"][0]
        document.getElementById("2").innerHTML = data["Question " + user_progress["qstn_number"]]["options"][1]
        document.getElementById("3").innerHTML = data["Question " + user_progress["qstn_number"]]["options"][2]
        document.getElementById("4").innerHTML = data["Question " + user_progress["qstn_number"]]["options"][3]
    }

    move_numbers()
}

let check_answr = function(answer){
    let given_answer = String(answer.innerHTML)
    let button_pressed = document.getElementById(answer.id)
    let num_box = document.getElementById("num-box-"+user_progress["qstn_number"])
    let right_answer = String(data["Question " + user_progress["qstn_number"]]["answer"])
    
    console.log("resposta enviada")
    console.log(given_answer)
    console.log(right_answer)
    
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
        
        // adds a point to the wrong questions
        user_progress["wrong"] = user_progress["wrong"] += 1
        
    }

    user_progress["qstn_number"] += 1
    // resets and prepares the quiz to the next question
    setTimeout(() => {

        button_pressed.classList.remove("right_answr")
        button_pressed.classList.remove("wrong_answr")
        button_pressed.classList.add("reset_answr")


        load_qstn()
    }, 1000);
    
    console.log(user_progress)
}

load_qstn()
// END Quiz Generation


