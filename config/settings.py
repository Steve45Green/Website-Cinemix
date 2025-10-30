from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent

INSTALLED_APPS = [
    # apps do Django...
    'django.contrib.staticfiles',  # importante para dev
    'core',                       # a tua app
]
# templates na pasta 'templates' (raiz do projeto)
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # <- aponta para a tua pasta
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
# Media (onde vai ficar os vídeos)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
# Ficheiros estáticos (CSS, JS, imagens)
STATIC_URL = '/static/'

# (opcional em desenvolvimento) onde colocas ficheiros estáticos do teu projeto
# Ex.: website/static/...
from pathlib import Path
STATICFILES_DIRS = [BASE_DIR / 'static']  # cria a pasta 'static' na raiz do projeto

# (apenas para produção, quando fores fazer collectstatic)
# STATIC_ROOT = BASE_DIR / 'staticfiles'
# Desenvolvimento
DEBUG = True
ALLOWED_HOSTS = ['127.0.0.1', 'localhost']
