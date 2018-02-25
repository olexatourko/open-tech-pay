#!/usr/bin/python
# -*- coding: utf-8 -*-

import unittest
from src import app, db
from src.models import *
from src.model_mappings import *
from src.high_level_methods import *

class TestHighLevelMethods(unittest.TestCase):

    def setUp(self):
        app.config.from_object('tests.config')
        db.session.close()
        db.drop_all()  # http://docs.sqlalchemy.org/en/latest/orm/extensions/declarative/basic_use.html
        db.create_all()

        self.roles = [
            Role('Web: Backend', listed=True),
            Role('Web: Frontend', listed=True),
            Role('Web: Full-Stack', listed=True)
        ]
        for role in self.roles: db.session.add(role)
        db.session.commit()

    def test_fetch_or_create_role(self):
        role = Role()
        role.id = self.roles[0].id
        found_role = fetch_or_create_role(role)
        assert found_role is not role
        assert found_role.id == role.id

        role = Role()
        role.name = self.roles[0].name
        found_role = fetch_or_create_role(role)
        assert found_role is not role
        assert found_role.id == self.roles[0].id

        role = Role()
        role.name = 'New Role'
        found_role = fetch_or_create_role(role)
        assert found_role is role
        assert found_role.id is None

if __name__ == '__main__':
    unittest.main()