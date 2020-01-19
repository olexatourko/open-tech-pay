#!/bin/bash
# export FLASK_ENV="development"
# flask run --port 5000 --host 0.0.0.0
gunicorn --bind 0.0.0.0:5000 --log-level debug wsgi:app