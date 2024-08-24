from . import views
from django.conf import settings
from django.urls import path, include
from django.conf.urls.static import static

urlpatterns = [
    # frontend
    path("", views.home, name="home"),
    path("create_quiz/", views.create, name="create"),
    path("quiz/", views.quiz, name="quiz"),
    
    # backend
    path("api/test/", views.api_test, name="api_test"),
    path("api/create/<username>/<ammount>", views.api_create, name="api_create"), # TODO: switch / with param
    path("api/read/<quiz_id>/", views.api_read, name="api_read")
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)