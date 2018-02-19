import os, sys
sys.path.insert(0, os.getcwd()) # This makes the app, db import work
from sqlalchemy import exc
from src import app, db
from src.models import PayRange, Role, EmailDomain
import datetime

def seed_db(database):
    try:
        # Add pay ranges
        for i in range(0, 145000 + 1, 5000):
            database.session.add(PayRange(lower=i, upper=i + 4999.99))

        # Add roles
        database.session.add(Role('Web: Backend'))
        database.session.add(Role('Web: Frontend'))
        database.session.add(Role('Web: Full-Stack'))
        database.session.add(Role('Web: Design'))
        database.session.add(Role('Software Developer'))

    except exc.SQLAlchemyError:
        database.session.rollback()

if __name__ == '__main__':
    seed_db(db)