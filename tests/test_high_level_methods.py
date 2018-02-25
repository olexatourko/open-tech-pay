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

if __name__ == '__main__':
    unittest.main()