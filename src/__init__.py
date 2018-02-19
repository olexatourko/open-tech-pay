from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
"""
Example run
export FLASK_APP=$(pwd)/src/application.py
export CONFIG_FILEPATH=$(pwd)/config.py
flask run
"""
app.config.from_envvar('CONFIG_FILEPATH')  # http://flask.pocoo.org/docs/0.12/config/
db = SQLAlchemy(app)