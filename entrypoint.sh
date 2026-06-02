#!/bin/sh

set -e

echo "Waiting for PostgreSQL..."

while ! nc -z "$POSTGRES_HOST" "$POSTGRES_PORT"; do
  sleep 1
done

echo "PostgreSQL is ready"

python manage.py migrate --noinput

if [ -f "backup.sql" ]; then
  echo "Importing data from backup.sql..."
  python backup.py || echo "backup.py failed or data already imported"
fi

python manage.py collectstatic --noinput

echo "Starting server..."

gunicorn finportfolio.wsgi:application --bind 0.0.0.0:8000