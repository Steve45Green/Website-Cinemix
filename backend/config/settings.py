import os
from pathlib import Path
# import login
# ---------------------------------
# Caminhos base
# ---------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent

# ---------------------------------
# Segurança / Debug
# ---------------------------------
# Em produção, define SECRET_KEY por variável de ambiente
SECRET_KEY = os.environ.get(
    "DJANGO_SECRET_KEY",
    "dev-insecure-key-change-me-only-for-local",  # usar apenas em DEV
)

# DEBUG: True em DEV; False em PROD (via variável de ambiente)
DEBUG = os.environ.get("DJANGO_DEBUG", "1") in ("1", "true", "True")

# Hosts permitidos
ALLOWED_HOSTS = [
    "127.0.0.1",
    "localhost",
    # adiciona o teu domínio em produção, por ex.: "cinemix.pt"
]
CSRF_TRUSTED_ORIGINS = [
    "http://127.0.0.1:8000",
    "http://127.0.0.1:8765",
    "http://localhost:8000",
    "http://localhost:8765",
    # Se tiveres React em dev:
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
    #"rest_framework"
    # A minha app
    "backend.core.apps.CoreConfig",


]

# ---------------------------------
# Middleware
# ---------------------------------
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# (Opcional) CORS para React em DEV
CORS_ALLOW_ALL_ORIGINS = True if DEBUG else False
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

# ---------------------------------
# URLs / WSGI / ASGI
# ---------------------------------
ROOT_URLCONF = "backend.config.urls"

WSGI_APPLICATION = "backend.config.wsgi.application"
ASGI_APPLICATION = "backend.config.asgi.application"

# ---------------------------------
# Templates
# ---------------------------------
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        # Se tiveres diretórios de templates no projeto:
        "DIRS": [BASE_DIR / "templates"],
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

# ---------------------------------
# Base de Dados
# - Postgres via variáveis de ambiente
# - Fallback para SQLite em DEV
# ---------------------------------
def env(name, default=None):
    return os.environ.get(name, default)

USE_POSTGRES = env("DB_ENGINE", "").lower().startswith("postgres")

if USE_POSTGRES:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": env("DB_NAME", "cinemix"),
            "USER": env("DB_USER", "cinemix"),
            "PASSWORD": env("DB_PASSWORD", "cinemix"),
            "HOST": env("DB_HOST", "127.0.0.1"),
            "PORT": env("DB_PORT", "5432"),
            # "OPTIONS": {"sslmode": "require"},  # se precisares
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

# ---------------------------------
# Password validation
# ---------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# ---------------------------------
# Internacionalização
# ---------------------------------
LANGUAGE_CODE = "pt-pt"
TIME_ZONE = "Europe/Lisbon"
USE_I18N = True
USE_TZ = True

# ---------------------------------
# Ficheiros estáticos e media
# ---------------------------------
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"  # para collectstatic em PROD

# Em DEV, podes também apontar para uma pasta local com assets:
STATICFILES_DIRS = [
    BASE_DIR / "static",  # cria se precisares
]

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# ---------------------------------
# Default primary key field
# ---------------------------------
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# ---------------------------------
# Emails (DEV: consola)
# ---------------------------------
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
# Em PROD, configurar SMTP:
# EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
# EMAIL_HOST = "smtp..."
# EMAIL_PORT = 587
# EMAIL_HOST_USER = env("EMAIL_HOST_USER", "")
# EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD", "")
# EMAIL_USE_TLS = True

# ---------------------------------
# Logging (o teu bloco, com pequena correção no formatter)
# ---------------------------------
LOG_DIR = BASE_DIR / "logs"
LOG_DIR.mkdir(exist_ok=True)

LOG_FILE_PATH = LOG_DIR / "app.log"
REQUESTS_LOG_FILE_PATH = LOG_DIR / "requests.log"

LOG_LEVEL = "DEBUG" if DEBUG else "INFO"

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,  # mantém loggers do Django ativos
    "formatters": {
        "verbose": {
            "format": "[{asctime}] [{levelname}] {name} ({module}:{lineno}) — {message}",
            "style": "{",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
        "simple": {
            "format": "{levelname}: {message}",
            "style": "{",
        },
        "colored": {  # útil no console em DEV
            # Atenção: '<' aqui tem de ser o carácter real, não '&lt;'
            "format": "\x1b[36m[{asctime}]\x1b[0m \x1b[33m{levelname:<8}\x1b[0m \x1b[35m{name}\x1b[0m — {message}",
            "style": "{",
            "datefmt": "%H:%M:%S",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "colored" if DEBUG else "simple",
            "level": LOG_LEVEL,
        },
        "file_app": {
            "class": "logging.handlers.RotatingFileHandler",
            "filename": str(LOG_FILE_PATH),
            "maxBytes": 5 * 1024 * 1024,  # 5 MB
            "backupCount": 5,
            "encoding": "utf-8",
            "formatter": "verbose",
            "level": LOG_LEVEL,
        },
        "file_requests": {
            "class": "logging.handlers.RotatingFileHandler",
            "filename": str(REQUESTS_LOG_FILE_PATH),
            "maxBytes": 5 * 1024 * 1024,
            "backupCount": 3,
            "encoding": "utf-8",
            "formatter": "verbose",
            "level": "INFO",
        },
        # Opcional: erros críticos para a consola apenas
        "console_errors": {
            "class": "logging.StreamHandler",
            "formatter": "verbose",
            "level": "ERROR",
        },
    },
    "loggers": {
        # A minha app
        "core": {
            "handlers": ["console", "file_app"],
            "level": LOG_LEVEL,
            "propagate": False,
        },
        # Logger do apps.py (usa __name__)
        "core.apps": {
            "handlers": ["console", "file_app"],
            "level": LOG_LEVEL,
            "propagate": False,
        },
        # Django geral
        "django": {
            "handlers": ["console", "file_app"],
            "level": "INFO" if DEBUG else "WARNING",
            "propagate": True,
        },
        # Erros de requests (500, etc.) — bom separar num ficheiro
        "django.request": {
            "handlers": ["console_errors", "file_requests"],
            "level": "ERROR",
            "propagate": False,
        },
        # SQL queries (muito verboso; para ativar so quando eu quiser)
        "django.db.backends": {
            "handlers": ["console"],
            "level": "DEBUG" if os.getenv("SQL_DEBUG") == "1" else "WARNING",
            "propagate": False,
        },
        # Segurança (CSRF, etc.)
        "django.security": {
            "handlers": ["console", "file_app"],
            "level": "WARNING",
            "propagate": False,
        },
    },
}