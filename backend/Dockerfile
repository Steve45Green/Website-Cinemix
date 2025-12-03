# 1. Imagem Base
FROM python:3.12-slim

# Define o diretório de trabalho
WORKDIR /app

# Previne que o Python crie ficheiros .pyc
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Instala dependências do sistema
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copia e instala as dependências do Python
COPY backend/requirements.txt /app/requirements.txt
RUN pip install --upgrade pip && pip install -r requirements.txt

# O código será montado através de um volume no docker-compose
COPY . /app/
