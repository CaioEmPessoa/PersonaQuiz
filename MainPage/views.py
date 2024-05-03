from django.shortcuts import render

# Create your views here.
def home(request):
    api_request = "steam"
    return render(request, "main_page.html")