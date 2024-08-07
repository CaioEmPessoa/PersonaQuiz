from . import views
from django.conf import settings
from django.urls import path, include
from django.conf.urls.static import static

urlpatterns = [
    # frontend
    path("", views.home, name="home"),
    path("create_quiz/", views.create, name="create"),
    path("quiz/", views.quiz, name="quiz"),
    
    # backend (copy from steam one, is a good base.)
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)