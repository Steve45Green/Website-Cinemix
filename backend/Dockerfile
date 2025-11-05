# Backend - Django (DEV)
FROM python:3.12-slim

# Variáveis para evitar cache e melhorar logs
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

# Instalar dependências do sistema
# - build-essential, libpq-dev: compilar psycopg/psycopg2
# - postgresql-client: fornece o pg_isready para o entrypoint esperar pela DB
# - libjpeg/zlib: comuns para Pillow (ImageField)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    postgresql-client \
    libjpeg62-turbo-dev \
    zlib1g-dev \
    curl \
  && rm -rf /var/lib/apt/lists/*

# Diretório de trabalho
WORKDIR /code

# Copiar requirements e instalar dependências Python
COPY requirements.txt /code/requirements.txt
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copiar o código do projeto para dentro do container
COPY .. /code

# Expor a porta interna que o Django usa
EXPOSE 8000

# O comando final é definido no docker-compose (runserver em DEV)
