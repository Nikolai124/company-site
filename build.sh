#!/usr/bin/env bash
# Сборка на Render: зависимости, статика, миграции, демо-контент и админ
set -o errexit

pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate
python manage.py seed_demo

# Админ создаётся из переменных DJANGO_SUPERUSER_*; если он уже есть, команда упадёт — это нормально
if [ -n "$DJANGO_SUPERUSER_USERNAME" ]; then
  python manage.py createsuperuser --no-input || true
fi
