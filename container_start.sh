#!/bin/bash
# update css and any assets first
sass --update sass:src/static/stylesheets
yarn install
# export FLASK_ENV="development"
# flask run --port 5000 --host 0.0.0.0
gunicorn --bind 0.0.0.0:5000 --log-level debug --reload wsgi:app