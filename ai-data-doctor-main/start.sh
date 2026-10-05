#!/usr/bin/env bash
set -euo pipefail

PORT="${PORT:-8000}"
WEB_CONCURRENCY="${WEB_CONCURRENCY:-1}"
GUNICORN_TIMEOUT="${GUNICORN_TIMEOUT:-300}"

python manage.py migrate --noinput

exec gunicorn \
  --bind "0.0.0.0:${PORT}" \
  --workers "${WEB_CONCURRENCY}" \
  --timeout "${GUNICORN_TIMEOUT}" \
  --access-logfile "-" \
  --error-logfile "-" \
  --worker-tmp-dir "/dev/shm" \
  wsgi:application
