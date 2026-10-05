#!/usr/bin/env bash
set -euo pipefail

python --version
python -m pip install --upgrade pip
python manage.py check
python manage.py migrate --noinput
python manage.py collectstatic --noinput
