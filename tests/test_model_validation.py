#!/usr/bin/python
# -*- coding: utf-8 -*-

import unittest
from src.models import *
from src.model_schemas import *


class TestValidation(unittest.TestCase):
    """ I'm only testing validation on Schemas that will be loaded from user input data. """

    def test_perk_schema_validation(self):
        # Happy path
        errors = PerkSchema().validate({
            'name': 'Test'
        })
        assert len(errors) == 0

        # Missing name
        errors = PerkSchema().validate({})
        assert len(errors) == 1

    def test_role_schema_validation(self):
        # Happy path
        errors = RoleSchema().validate({
            'name': 'Test'
        })
        assert len(errors) == 0

        # Missing name
        errors = RoleSchema().validate({})
        assert len(errors) == 1

    def test_tech_schema_validation(self):
        # Happy path
        errors = TechSchema().validate({
            'name': 'Test'
        })
        assert len(errors) == 0

        # Missing name
        errors = TechSchema().validate({})
        assert len(errors) == 1

    def test_submission_schema_validation(self):
        # Happy path
        errors = SubmissionSchema().validate({
            'salary': 60000,
            'email': 'test@test.com',
            'years_experience': 5,
            'number_of_employers': 3,
            'years_with_current_employer': 1
        })
        assert len(errors) == 0

        # Invalid email cases
        errors = SubmissionSchema(many=True).validate([
            {
                'email': 'Invalid',
                'years_experience': 5,
                'number_of_employers': 3,
                'years_with_current_employer': 1
            },
            {
                'years_experience': 5,
                'number_of_employers': 3,
                'years_with_current_employer': 1
            }

        ])
        assert len(errors) == 2

        # Invalid years experience cases
        errors = SubmissionSchema(many=True).validate([
            {
                'email': 'test@test.com',
                'years_experience': 'This should be an integer',
                'number_of_employers': 3,
                'years_with_current_employer': 1
            },
            {
                'email': 'test@test.com',
                'number_of_employers': 3,
                'years_with_current_employer': 1
            }

        ])
        assert len(errors) == 2

        # years_with_current_employer > years_experience
        errors = SubmissionSchema().validate({
            'salary': 60000,
            'email': 'test@test.com',
            'years_experience': 1,
            'number_of_employers': 1,
            'years_with_current_employer': 2
        })
        assert len(errors) == 2

if __name__ == '__main__':
    unittest.main()