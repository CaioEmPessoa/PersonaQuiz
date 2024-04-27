from django.shortcuts import render
STYLE_PATH = "css/steam_style.css"
ICON_PATH = "img/steam_logo.png"

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