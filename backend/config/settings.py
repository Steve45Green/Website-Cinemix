import os
from pathlib import Path

# ---------------------------------
# Caminhos base
# ---------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent

# ---------------------------------
# Segurança / Debug
# ---------------------------------
SECRET_KEY = os.environ.get(
    "DJANGO_SECRET_KEY",
    "dev-insecure-key-change-me-only-for-local",
)
DEBUG = os.environ.get("DJANGO_DEBUG", "1") in ("1", "true", "True")

ALLOWED_HOSTS = [
    "127.0.0.1",
    "localhost",
]
CSRF_TRUSTED_ORIGINS = [
    "http://127.0.0.1:8000",
    "http://127.0.0.1:8765",
    "http://localhost:8000",
    "http://localhost:8765",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

# ---------------------------------
# Apps
# ---------------------------------
INSTALLED_APPS = [
    # Core Django
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # Apps de terceiros
    "corsheaders",
    "rest_framework",

    # A minha app
    "backend.core.apps.CoreConfig",
]

# ---------------------------------
# Middleware
# ---------------------------------
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    # Corsheaders deve vir ANTES de CommonMiddleware
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# ---------------------------------
# Configuração CORS
# ---------------------------------
CORS_ALLOW_ALL_ORIGINS = True # Para desenvolvimento, mais fácil
# Em produção, usa isto:
# CORS_ALLOWED_ORIGINS = [
#     "http://localhost:3000", # O teu frontend
#     "http://127.0.0.1:3000",
#     "http://o-teu-dominio.com",
# ]

# ---------------------------------
# URLs / WSGI / ASGI
# ---------------------------------
ROOT_URLCONF = "backend.config.urls"
WSGI_APPLICATION = "backend.config.wsgi.application"
ASGI_APPLICATION = "backend.config.asgi.application"

# ---------------------------------
# Templates / Internacionalização
# ---------------------------------
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR.parent / "frontend/dist"], # Aponta para o build do React/Vite
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

LANGUAGE_CODE = "pt-pt"
TIME_ZONE = "Europe/Lisbon"
USE_I18N = True
USE_TZ = True

# ---------------------------------
# Ficheiros Estáticos (Static) e Média
# ---------------------------------
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR.parent / "staticfiles"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR.parent / "media"

# ---------------------------------
# Base de Dados (exemplo com fallback para SQLite)
# ---------------------------------
# Lógica para usar Postgres (Docker) ou SQLite (local fallback)
USE_POSTGRES = os.environ.get("USE_POSTGRES", "1") in ("1", "true", "True")

if USE_POSTGRES:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": os.environ.get("DB_NAME", "cinemix"),
            "USER": os.environ.get("DB_USER", "cinemix"),
            "PASSWORD": os.environ.get("DB_PASS", "cinemix"),
            "HOST": os.environ.get("DB_HOST", "127.0.0.1"), # 'db' no Docker
            "PORT": os.environ.get("DB_PORT", "5432"),
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR.parent / "db.sqlite3", # Na raiz do projeto
        }
    }

# ---------------------------------
# Rest Framework
# ---------------------------------
REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.AllowAny",
    ],
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 20,
}

# ---------------------------------
# AutoField e Logging
# ---------------------------------
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "{levelname} {asctime} {module} {message}",
            "style": "{",
        },
        "simple": {
            "format": "{levelname} {message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "simple",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "INFO",
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": os.getenv("DJANGO_LOG_LEVEL", "INFO"),
            "propagate": False,
        },
    },
}
