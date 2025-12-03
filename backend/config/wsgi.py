# -*- coding: utf-8 -*-
"""
Configuração WSGI (Web Server Gateway Interface) para o projeto.

Este ficheiro serve como o ponto de entrada para servidores web compatíveis com WSGI,
que é o padrão tradicional para correr aplicações Python síncronas.

O `get_wsgi_application()` carrega e retorna a aplicação WSGI do Django, que
depois pode ser utilizada por um servidor como o Gunicorn ou o Apache com mod_wsgi.
"""
import os
from django.core.wsgi import get_wsgi_application

# Define a variável de ambiente `DJANGO_SETTINGS_MODULE`.
# Esta linha garante que o Django sabe onde encontrar o ficheiro de configurações (settings.py)
# do projeto. É um passo fundamental para a aplicação funcionar.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.config.settings")

# Obtém a aplicação WSGI.
# A função `get_wsgi_application` inspeciona a variável `DJANGO_SETTINGS_MODULE`,
# carrega as configurações e retorna uma aplicação WSGI pronta a ser servida.
application = get_wsgi_application()
