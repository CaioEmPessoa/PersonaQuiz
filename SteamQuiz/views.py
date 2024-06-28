from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from .models import Quiz, Option
import json

from .src import user_data

STYLE_PATH = "css/steam_style.css"
ICON_PATH = "img/steam_logo.png"

SteamAPI = user_data.SteamData()


# Create your views here.
def home(request):
    api_request = "steam"

    return render(request, "index.html", 
                  {
                      "style_path":STYLE_PATH,
                      "icon_path":ICON_PATH
                  })

def read(request, id="none"):
    return render(request, "read_quiz.html",
                  {
                      "style_path":STYLE_PATH,
                      "icon_path":ICON_PATH
                  })

def create(request):
    return render(request, "create_quiz.html",
                  {
                      "style_path": STYLE_PATH,
                      "icon_path":ICON_PATH
                  })

def quiz(request):
    return render(request, "quiz.html",
                  {
                      "style_path": STYLE_PATH,
                      "icon_path":ICON_PATH
                  })

# API REQUESTS

def api_test(request):
    return HttpResponse('sucesso!')

def api_create(request, username, ammount):
    data = SteamAPI.user_data(username, int(ammount))
    return JsonResponse(data)

def api_read(request, quiz_id):
    try:
        with open(f"{SteamAPI.user_data_location}/{quiz_id}.json", "r") as load_file:
            data = json.load(load_file)
            data["status"] = "Quiz Carregado!"
            return JsonResponse(data)
    except:
        return(JsonResponse({"status":"Esse quiz não existe! Verifique seu código."}))