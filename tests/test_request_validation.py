#!/usr/bin/python
# -*- coding: utf-8 -*-

import unittest

from src import app
from src.models import *
from src.request_schemas import SubmissionRequestSchema
from utils.seeding.seed_core import seed_core


class TestRequestValidation(unittest.TestCase):
    def setUp(self):
        app.config.from_object('tests.config')
        db.session.close()
        db.drop_all()
        db.create_all()
        seed_core(db)

    def test_valid_request_1(self):
        request_dict = {
            'salary': 60000,
            'employment_type': EmploymentType.query.first().id,
            'location': Location.query.first().id,
            'years_with_current_employer': 1,
            'years_experience': 1,
            'roles': [
                {
                    'id': Role.query.first().id
                }
            ],
            'techs': [],
            'perks': [],
            'education': Education.query.first().id,
            'email': 'test@test.com'
        }
        assert len(SubmissionRequestSchema().validate(request_dict)) == 0

    def test_invalid_request_1(self):
        """ Missing roles """
        request_dict = {
            'salary': 60000,
            'employment_type': EmploymentType.query.first().id,
            'location': Location.query.first().id,
            'years_with_current_employer': 1,
            'years_experience': 1,
            'roles': [],
            'techs': [],
            'perks': [],
            'education': Education.query.first().id,
            'email': 'test@test.com'
        }
        assert len(SubmissionRequestSchema().validate(request_dict)) > 0

    def test_invalid_request_2(self):
        """ years_with_current_employer > years_experience """
        request_dict = {
            'salary': 60000,
            'employment_type': EmploymentType.query.first().id,
            'location': Location.query.first().id,
            'years_with_current_employer': 2,
            'years_experience': 1,
            'roles': [
                {
                    'id': Role.query.first().id
                }
            ],
            'techs': [],
            'perks': [],
            'education': Education.query.first().id,
            'email': 'test@test.com'
        }
        assert len(SubmissionRequestSchema().validate(request_dict)) > 0

    def test_invalid_request_3(self):
        """ email with '+' in it """
        request_dict = {
            'salary': 60000,
            'employment_type': EmploymentType.query.first().id,
            'location': Location.query.first().id,
            'years_with_current_employer': 1,
            'years_experience': 1,
            'roles': [
                {
                    'id': Role.query.first().id
                }
            ],
            'techs': [],
            'perks': [],
            'education': Education.query.first().id,
            'email': 'test+malicious.intent@test.com'
        }
        assert len(SubmissionRequestSchema().validate(request_dict)) > 0

    def test_invalid_request_4(self):
        """ Salary < 0 """
        request_dict = {
            'salary': -1000,
            'employment_type': EmploymentType.query.first().id,
            'location': Location.query.first().id,
            'years_with_current_employer': 1,
            'years_experience': 1,
            'roles': [
                {
                    'id': Role.query.first().id
                }
            ],
            'techs': [],
            'perks': [],
            'education': Education.query.first().id,
            'email': 'test@test.com'
        }
        assert len(SubmissionRequestSchema().validate(request_dict)) > 0

    def test_invalid_request_5(self):
        """ Salary < 0 """
        request_dict = {
            'salary': 1000001,
            'employment_type': EmploymentType.query.first().id,
            'location': Location.query.first().id,
            'years_with_current_employer': 1,
            'years_experience': 1,
            'roles': [
                {
                    'id': Role.query.first().id
                }
            ],
            'techs': [],
            'perks': [],
            'education': Education.query.first().id,
            'email': 'test@test.com'
        }
        assert len(SubmissionRequestSchema().validate(request_dict)) > 0

if __name__ == '__main__':
    unittest.main()