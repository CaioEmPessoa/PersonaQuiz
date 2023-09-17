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

// display data
const refresh = function(){
        if (user_progress["qstn_number"] == data["qstn_count"]+1){
            document.getElementById("title").innerHTML = "acabo.<br>Pontuação: " + user_progress["right"]

        } else {
        document.getElementById("title").innerHTML = data["Question " + user_progress["qstn_number"]]["question"]

        document.getElementById("1").innerHTML = data["Question " + user_progress["qstn_number"]]["options"][0]
        document.getElementById("2").innerHTML = data["Question " + user_progress["qstn_number"]]["options"][1]
        document.getElementById("3").innerHTML = data["Question " + user_progress["qstn_number"]]["options"][2]
        document.getElementById("4").innerHTML = data["Question " + user_progress["qstn_number"]]["options"][3]
    }
}

const check_answr = function(answer){
    console.log("resposta enviada")
    console.log(answer.innerHTML)
    console.log(data["Question 1"]["answer"])
    
    // caso a resposta esteja correta...
    if (answer.innerHTML == data["Question 1"]["answer"]){
        console.log("acerto!")
        
        // adds a point to the right questions
        user_progress["right"] = user_progress["right"] += 1
        
    } 
    
    // caso a resposta esteja errada...
    else {
        // adds a point to the wrong questions
        user_progress["wrong"] = user_progress["wrong"] += 1
        console.log("errou!")
    }

    user_progress["qstn_number"] += 1
    refresh()
    console.log(user_progress)
}

refresh()
// END Quiz Generation


