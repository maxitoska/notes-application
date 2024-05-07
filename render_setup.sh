#!/bin/bash
set -e


pip install -r requirements.txt

python manage.py makemigrations

python manage.py migrate

python manage.py collectstatic --noinput

gunicorn notes_application_service.wsgi:application --bind 0.0.0.0:$PORT
