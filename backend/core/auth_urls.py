# backend/core/auth_urls.py

from django.urls import path
from .views import UserRegistrationView, UserMeView

urlpatterns = [
    # Rota para criar um novo utilizador
    # POST /api/auth/register/
    path("register/", UserRegistrationView.as_view(), name="register"),

    # Rota para obter o perfil do utilizador autenticado
    # GET /api/auth/me/
    path("me/", UserMeView.as_view(), name="me"),
]