from . import views
from django.conf import settings
from django.urls import path, include
from django.conf.urls.static import static

urlpatterns = [
    path("", views.home, name="home"),
    path("read_quiz/<str:id>", views.read, name="read"),
    path("create_quiz/", views.create, name="create")
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)