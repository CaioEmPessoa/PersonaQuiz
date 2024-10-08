const currentQuiz = "/" + window.location.pathname.split("/")[1]
const apiUrl = currentQuiz + "/api"

// the slider output <--------------------------------------------------<
let slider = document.getElementById("questionSlider");
let output = document.getElementById("sliderOutput");
output.innerHTML = slider.value // Display the default slider value

// Update the current slider value (each time you drag the slider handle)
var qstn_ammount = 5
slider.oninput = function() {
  qstn_ammount = this.value
  output.innerHTML = this.value
}
// >----------------------------------------------------> END SLIDER

// START json data <------------------------------------------------------------------------------<
let send_button = document.getElementById("enviar");
let loading = document.getElementById("loading")
let error_label = document.getElementById("error")

let create_quiz = function(){
  let nameEntry = document.getElementById("usernameEntry").value

  if (nameEntry[nameEntry.length-1] != "/"){
    nameEntry = nameEntry + "/"
  }

  // split link and get the last part of it (name or id)

  nameEntry = nameEntry.split("/")
  nameEntry = nameEntry[nameEntry.length-2]
  
  if(nameEntry==undefined || nameEntry==""){
    return error_label.innerHTML = "Insira um link válido."
  }

  send_button.style.display = "none"
  loading.style.display = "inline-block"

  if (qstn_ammount==0){
    qstn_ammount = 1
  }

  var r_url = `${apiUrl}/create/${nameEntry}/${qstn_ammount}/`
  if (currentQuiz == "/LastfmQuiz") {
    r_url += document.getElementById("period").value
  }
  
  fetch(`${apiUrl}/test`)
  .then( response => {
    fetch(r_url).then(response => response.json()).then(
      function(data){
        // se o data retornar um erro, ele mostra o erro.
        if(data["status"] != "Quiz Criado!"){
          send_button.style.display = "inline-block"
          loading.style.display = "none"
          document.getElementById("error").innerHTML = data["status"]
          return
          
        }
        if (data["status"] == "Quiz Criado!") {
          document.getElementById("error").style.color = "#32CD32"
          let sharelink = document.getElementById("sharelink")

          error_label.innerHTML = "Quiz feito! Você pode acessar ou compartilhar ele no seguinte link:"
          console.log(currentQuiz)
          console.log(apiUrl)
          console.log("WJKHDKHJADS")
          sharelink.innerHTML = `${window.location.origin}${apiUrl.slice(0, -4)}/?id=${data["qstn_id"]}`
          sharelink.href = `${window.location.origin}${apiUrl.slice(0, -4)}/?id=${data["qstn_id"]}`
          
          send_button.style.display = "inline-block"
          loading.style.display = "none"
          return
        }
      });
    })
    .catch(error => {
      send_button.style.display = "inline-block"
      loading.style.display = "none"
      return error_label.innerHTML = "Erro do servidor, tente novamente mais tarde."
    });
}
  //>-----------------------------------------------------------------------------> END json data
 
send_button.onclick = () => create_quiz()
let usernameEntry = document.getElementById("usernameEntry")

usernameEntry.addEventListener("keydown", function(event) {
    if (event.key === "Enter") {
        if (usernameEntry === document.activeElement) {
          create_quiz()
        }
    }
})