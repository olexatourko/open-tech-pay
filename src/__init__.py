from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from werkzeug.contrib.fixers import ProxyFix

app = Flask(__name__)

# HTTPS fix when using reverse proxy
# https://stackoverflow.com/questions/47603264/flask-why-are-some-endpoints-not-https/47603388#47603388
app.wsgi_app = ProxyFix(app.wsgi_app)

"""
Example run
export FLASK_APP=$(pwd)/src/application.py
export CONFIG_FILEPATH=$(pwd)/config.py
flask run
"""
app.config.from_envvar('CONFIG_FILEPATH')  # http://flask.pocoo.org/docs/0.12/config/
db = SQLAlchemy(app)
