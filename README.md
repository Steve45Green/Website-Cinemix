
# 🎬 Website Cinemix
[![Status](https://img.shields.io/badge/status-active-success.svg)]()
[![License](https://img.shields.io/badge/license-MIT-blue.svg)]()
[![Backend](https://img.shields.io/badge/backend-Django-092E20.svg)]()
[![Frontend](https://img.shields.io/badge/frontend-React%20%2B%20Vite-61DAFB.svg)]()
[![Database](https://img.shields.io/badge/database-PostgreSQL-336791.svg)]()
[![Containers](https://img.shields.io/badge/containers-Docker-2496ED.svg)]()
[![Language](https://img.shields.io/badge/language-TypeScript-blue.svg)]()

> Plataforma web para gestão de filmes, com **Django (backend)**, **React + Vite (frontend)**, **PostgreSQL** e **Docker Compose**. Inclui listagem de filmes, pesquisa, reservas e painel administrativo.

---

## 📑 Índice
- [✨ Funcionalidades](#-funcionalidades)
- [🏗️ Arquitetura do Projeto](#️-arquitetura-do-projeto)
- [🛠️ Stack Tecnológica](#-stack-tecnológica)
- [📦 Pré-requisitos](#-pré-requisitos)
- [⚡ Arranque Rápido (Docker)](#-arranque-rápido-docker)
- [🔐 Configuração (.env)](#-configuração-env)
- [📂 Estrutura do Projeto](#-estrutura-do-projeto)
- [🧪 Testes](#-testes)
- [🛣️ Roadmap](#️-roadmap)
- [🤝 Contribuir](#-contribuir)
- [📄 Licença](#-licença)
- [👤 Autores](#-autores)

---

## ✨ Funcionalidades
- ✅ Catálogo de filmes (cartaz, destaques)
- ✅ Pesquisa e filtros (título, género)
- ✅ Detalhes do filme (sinopse, trailer, posters)
- ✅ Sistema de reservas
- ✅ Autenticação e perfis
- ✅ Painel administrativo
- ✅ Integração Django + React via Vite e `templatetags/vite.py`

---

## 🏗️ Arquitetura do Projeto
A aplicação é composta por:
- **Frontend:** React + Vite (TypeScript) para interface do utilizador.
- **Backend:** Django + Django REST Framework para lógica de negócio e API.
- **Base de Dados:** PostgreSQL para persistência.
- **Infraestrutura:** Docker Compose para orquestração dos serviços.

### Diagrama
```
┌────────────────────┐        HTTP/JSON        ┌────────────────────┐
│  React + Vite      │  <--------------------> │  Django + DRF      │
│  (Frontend)        │                         │  (Backend API)     │
└─────────┬──────────┘                         └─────────┬──────────┘
          │                                             │
          │                                             ▼
          │                                     ┌────────────────────┐
          │                                     │    PostgreSQL      │
          │                                     └────────────────────┘
          │
          ▼
┌────────────────────┐
│    Docker Compose  │  (Orquestra todos os serviços)
└────────────────────┘
```

Cada serviço é containerizado:
- `frontend` → React app servida via Vite.
- `backend` → Django app com API REST.
- `db` → PostgreSQL com volume persistente.

Opcionalmente, pode incluir **Nginx** como proxy reverso para produção.

---

## 🛠️ Stack Tecnológica
- **Backend:** Django, Django REST Framework
- **Frontend:** React + Vite + TypeScript
- **Base de Dados:** PostgreSQL
- **Infra:** Docker & Docker Compose
- **Estilos:** CSS (e/ou Tailwind)
- **Qualidade:** Black, Flake8, ESLint, Prettier

---

## 📦 Pré-requisitos
- Docker & Docker Compose
- Node.js (para desenvolvimento frontend)
- Python 3.x (para desenvolvimento backend)

---

## ⚡ Arranque Rápido (Docker)
```bash
git clone https://github.com/Steve45Green/Website-Cinemix.git
cd Website-Cinemix

# Criar .envs
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env

# Subir serviços
docker compose up -d --build

# Migrar BD e criar admin
docker compose exec backend python manage.py migrate
docker compose exec backend python manage.py createsuperuser
```

---

## 🔐 Configuração (.env)
**Backend – `backend/.env`**
```
DJANGO_SECRET_KEY=altera_esta_chave
DJANGO_DEBUG=1
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1

POSTGRES_DB=cinemix
POSTGRES_USER=cinemix
POSTGRES_PASSWORD=cinemix
DATABASE_URL=postgres://cinemix:cinemix@db:5432/cinemix

CSRF_TRUSTED_ORIGINS=http://localhost:8000,http://localhost:5173
CORS_ALLOWED_ORIGINS=http://localhost:5173,http://localhost:3000

DJANGO_STATIC_ROOT=/app/staticfiles
DJANGO_MEDIA_ROOT=/app/media
```

**Frontend – `frontend/.env`**
```
VITE_API_URL=http://localhost:8000/api
```

---

## 📂 Estrutura do Projeto
```
Website-Cinemix/
├─ config/                # settings.py, urls.py, asgi.py, wsgi.py
├─ core/                  # models.py, views.py, serializers.py, tests.py
├─ templates/             # base.html, index.html, movie_detail.html, play.html
├─ templatetags/          # vite.py (integração Vite)
├─ static/                # css/, js/, images/
├─ media/                 # uploads (posters, etc.)
├─ frontend/
│  ├─ public/
│  ├─ src/
│  │  ├─ components/      # Header.tsx, Hero.tsx, MovieCard.tsx, MovieCarousel.tsx
│  │  ├─ styles/
│  │  ├─ App.tsx
│  │  └─ main.tsx
│  ├─ index.html
│  ├─ package.json
│  ├─ tsconfig.json
│  └─ vite.config.ts
└─ docker-compose.yml
```

---

## 🧪 Testes
**Backend**
```bash
docker compose exec backend python manage.py test
```
**Frontend**
```bash
docker compose exec frontend npm test
```

---

## 🛣️ Roadmap
- [ ] Documentação da API (Swagger / drf-spectacular)
- [ ] CI/CD (GitHub Actions)

---

## 🤝 Contribuir
1. Fazer fork
2. `git checkout -b feat/nova-feature`
3. `git commit -m "feat: descrição"`
4. `git push origin feat/nova-feature`
5. Abrir Pull Request

---

## 📄 Licença
MIT © 2025 [Steve45Green]

---

## 👤 Autores
- José Ameixa — Full Stack Developer
- Diogo Vaz - Full Stack Developer
