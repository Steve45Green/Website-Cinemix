# -*- coding: utf-8 -*-
"""
Configuração ASGI (Asynchronous Server Gateway Interface) para o projeto.

Este ficheiro serve como o ponto de entrada para servidores web compatíveis com ASGI,
que são necessários para suportar funcionalidades assíncronas do Django, como
o Django Channels (usado para WebSockets, etc.).

O `get_asgi_application()` carrega e retorna a aplicação ASGI do Django, que
depois pode ser utilizada por um servidor como o Daphne ou Uvicorn.
"""
import os
from django.core.asgi import get_asgi_application

# Define a variável de ambiente `DJANGO_SETTINGS_MODULE`.
# Esta linha garante que o Django sabe onde encontrar o ficheiro de configurações (settings.py)
# do projeto. É crucial para que a aplicação funcione corretamente.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.config.settings")

# Obtém a aplicação ASGI.
# A função `get_asgi_application` inspeciona a variável `DJANGO_SETTINGS_MODULE`,
# carrega as configurações e retorna uma aplicação ASGI pronta a ser servida.
application = get_asgi_application()
