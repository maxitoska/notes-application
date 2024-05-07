#!/bin/bash
set -e

# Install Python dependencies
pip install -r requirements.txt

# Run Django database migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput

# Start the Django server
gunicorn notes_application_service.wsgi:application --bind 0.0.0.0:$PORT
