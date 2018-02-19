
from flask_migrate import Migrate
from src import app, db
from src.models import *

migrate = Migrate(app, db)
