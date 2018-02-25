from src import db
from models import *


def fetch_or_create_role(role):
    if role.id is not None:
        found_role = Role.query.filter(Role.id == role.id).first()
        return found_role

    if role.name is not None:
        found_role = Role.query.filter(Role.name == role.name).first()
        if found_role:
            return found_role

        db.session.add(role)
        return role

    return None # Should throw an exception instead
