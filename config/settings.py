# config/settings.py
from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent

# --- Desenvolvimento ---
DEBUG = True
ALLOWED_HOSTS = ["127.0.0.1", "localhost"]

# --- Apps instaladas ---
INSTALLED_APPS = [
    # Django…
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # Terceiros 
    "rest_framework",                   

    # apps
    "core",
]
# --- Middleware (necessário para admin/sessões/mensagens, etc.) ---
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"
WSGI_APPLICATION = "config.wsgi.application"

# --- Internacionalização (PT-PT) ---
LANGUAGE_CODE = "pt-pt"
TIME_ZONE = "Europe/Lisbon"
USE_I18N = True
USE_TZ = True

# --- Base de dados (DEV: SQLite) ---
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# --- evita o warning do AutoField ---
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# --- Templates ---
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],  # website/templates
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# --- Ficheiros estáticos (CSS/JS/imagens) ---
STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'core', 'static')]# website/static (em desenvolvimento)

# --- Media (uploads, p.ex. vídeos) ---
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# ---Config DRF básica ---
REST_FRAMEWORK = {
    "DEFAULT_RENDERER_CLASSES": ["rest_framework.renderers.JSONRenderer"],
    "DEFAULT_PARSER_CLASSES": ["rest_framework.parsers.JSONParser"],
}
# config/settings.py

SECRET_KEY = "vi+0n)_#5ta=s!+&(1oj+&-3bhr1gsji-!&y)1^31v7j%j^kf7"
