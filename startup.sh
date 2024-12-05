#!/bin/bash
python manage.py collectstatic --noinput
python manage.py migrate
gunicorn --workers 2 ClientTracker.wsgi