import os
from pathlib import Path
from datetime import timedelta # 

# ---------------------------------
# Caminhos base
# ---------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent
# (Resto das configurações de caminhos...)

# ---------------------------------
# Segurança / Debug
# ---------------------------------
SECRET_KEY = os.environ.get(
    "DJANGO_SECRET_KEY",
    "dev-insecure-key-change-me-only-for-local",
)
DEBUG = os.environ.get("DJANGO_DEBUG", "1") in ("1", "true", "True")

ALLOWED_HOSTS = ["127.0.0.1", "localhost"]
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
    "rest_framework_simplejwt", # <-- NOVO
    "drf_spectacular",          # <-- NOVO

    # A minha app
    "backend.core.apps.CoreConfig",
]

# ---------------------------------
# Middleware
# ---------------------------------
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware", # Corsheaders
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# ---------------------------------
# Configuração CORS
# ---------------------------------
CORS_ALLOW_ALL_ORIGINS = True # Simplificado para DEV

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
        "DIRS": [],
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
# Base de Dados
# ---------------------------------
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
            "NAME": BASE_DIR.parent / "db.sqlite3",
        }
    }

# ---------------------------------
# AutoField e Logging
# ---------------------------------
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
# (A tua configuração de LOGGING fica aqui...)
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "{levelname} {asctime} {module} {message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "INFO",
    },
}

# =================================
#       DJANGO REST FRAMEWORK (ATUALIZADO)
# =================================
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        # Priorizar JWT para pedidos de API
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        # SessionAuth apenas para usar no Admin/Browsable API
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        # Por defeito, utilizadores anónimos só podem ler
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ),
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema', # Para Documentação
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 20,
}

# =================================
#            SIMPLE JWT (NOVO)
# =================================
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ALGORITHM': 'HS256',
    'AUTH_HEADER_TYPES': ('Bearer',), # O frontend deve enviar 'Bearer <token>'
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
}

# =================================
#    DRF SPECTACULAR (NOVO)
# =================================
SPECTACULAR_SETTINGS = {
    'TITLE': 'Cinemix API',
    'DESCRIPTION': 'Documentação para a API do projeto Cinemix.',
    'VERSION': 'v1',
    'SERVE_INCLUDE_SCHEMA': False,
    'SWAGGER_UI_SETTINGS': {
        'deepLinking': True,
        'persistAuthorization': True,
        'displayRequestDuration': True,
    },
}

