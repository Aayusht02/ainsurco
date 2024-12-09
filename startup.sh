#!/bin/bash
python manage.py collectstatic --noinput
python manage.py migrate
waitress-serve --port=8000 ClientTracker.wsgi:application