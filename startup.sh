#!/bin/bash
python manage.py collectstatic --noinput
gunicorn --workers 2 ClientTracker.wsgi:application
