#!/usr/bin/python
# -*- coding: utf-8 -*-

import unittest
from src import app, db
from src.models import *
from src.model_mappings import *


class TestModelMappings(unittest.TestCase):

    def setUp(self):
        pass

    def test_dict_to_model(self):
        """ Test dict -> model mapping on Role (Tech/Perk should work the same) """
        role_dict = {
            'id': 3,
            'name': 'Role 1'
        }
        schema = RoleSchema()
        role = schema.load(role_dict).data
        assert role.id == role_dict['id']
        assert role.name == role_dict['name']

        role_dict = {
            'name': 'Role 3',
        }
        schema = RoleSchema()
        role = schema.load(role_dict).data
        assert not role.id
        assert role.name == role_dict['name']


if __name__ == '__main__':
    unittest.main()