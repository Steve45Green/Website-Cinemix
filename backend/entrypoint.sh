#!/usr/bin/env sh
set -eu

: "${DB_HOST:=db}"
: "${DB_PORT:=5432}"
: "${POSTGRES_USER:=cinemix}"

echo "Aguarda pela DB em ${DB_HOST}:${DB_PORT}..."
ATTEMPTS=30
i=0
until pg_isready -h "$DB_HOST" -p "$DB_PORT" -U "$POSTGRES_USER" >/dev/null 2>&1; do
  i=$((i+1))
  if [ "$i" -ge "$ATTEMPTS" ]; then
    echo "Timeout à espera da DB"
    exit 1
  fi
  echo "DB ainda não disponível... ($i/$ATTEMPTS)"
  sleep 1
done

python manage.py migrate --noinput || true
python manage.py collectstatic --noinput || true

# Em DEV: autoreload
exec python manage.py runserver 0.0.0.0:8000
# exec gunicorn config.asgi:application --workers ${GUNICORN_WORKERS:-3} --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000 --timeout ${GUNICORN_TIMEOUT:-120}
