// Quiz Generation

// read data
var data = localStorage['quiz_data'];
if (data==undefined) {
    console.log("Sem data.")
    
    const queryString = window.location.search;
    const urlParams = new URLSearchParams(queryString);
    const quiz_id = urlParams.get('id')
    
    window.location.href = "/view/quiz.html?id=" + quiz_id
}

data = JSON.parse(data)

localStorage.removeItem('quiz_data');


const qstn_numb = Array.from({length: data["qstn_count"]}, (_, i) => i + 1)

for(let x of qstn_numb){
    if (x <= 5){
        const para = document.createElement("p");
        const node = document.createTextNode(x);
        para.appendChild(node);
        
        const element = document.getElementById("numbers");
        element.appendChild(para);
    } else {
        const para = document.createElement("p");
        const node = document.createTextNode("...");
        para.appendChild(node);
        
        const element = document.getElementById("numbers");
        element.appendChild(para);
        break
    }
}

if (user_progress==undefined) {
    console.log("Sem Progresso.")
    var user_progress = {
        "right":0,
        "wrong":0,
        "qstn_number":1,
    }
}
console.log(user_progress)


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
}

let check_answr = function(answer){
    let button_pressed = document.getElementById(answer.id)
    let given_answer = String(answer.innerHTML)
    let right_answer = String(data["Question " + user_progress["qstn_number"]]["answer"])

    console.log("resposta enviada")
    console.log(given_answer)
    console.log(right_answer)
    
    answers_div.style.transitionProperty = "background-color"
    answers_div.style.transitionDuration = "1s"
    
    // caso a resposta esteja correta...

    if (given_answer == right_answer){
        console.log("acerto!")
        
        button_pressed.style.backgroundColor = "lime"
        
        // adds a point to the right questions
        user_progress["right"] = user_progress["right"] += 1
        
    } 
    
    // caso a resposta esteja errada...
    else {
        // adds a point to the wrong questions
        user_progress["wrong"] = user_progress["wrong"] += 1
        
        button_pressed.style.backgroundColor = "red"
        
        console.log("errou!")
    }

    user_progress["qstn_number"] += 1
    setTimeout(() => { load_qstn(); button_pressed.style.backgroundColor = "#a7a7a7"; }, 1000);
    
    console.log(user_progress)
}

load_qstn()
// END Quiz Generation


