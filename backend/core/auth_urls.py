# -*- coding: utf-8 -*-
"""
Definição das rotas (URLs) para a gestão de autenticação e utilizadores.

Este ficheiro agrupa os endpoints relacionados com o registo e a consulta
de perfis de utilizador. Estas rotas são normalmente incluídas no `urls.py`
principal do projeto sob um prefixo como `/api/auth/`.
"""
from django.urls import path
from .views import UserRegistrationView, UserMeView

# A lista de padrões de URL para a autenticação.
urlpatterns = [
    # Rota para o registo de um novo utilizador.
    # Aceita pedidos POST para /api/auth/register/
    # A view `UserRegistrationView` trata da lógica de criação.
    path("register/", UserRegistrationView.as_view(), name="register"),

    # Rota para obter o perfil do utilizador atualmente autenticado.
    # Aceita pedidos GET para /api/auth/me/
    # A view `UserMeView` retorna os dados do utilizador que faz o pedido.
    # Requer que o utilizador esteja autenticado (com um token válido).
    path("me/", UserMeView.as_view(), name="me"),
]
