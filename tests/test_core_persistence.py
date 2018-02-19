#!/usr/bin/python
# -*- coding: utf-8 -*-

import unittest
from src import app, db
from src.models import *

class TestCorePersistence(unittest.TestCase):


    def setUp(self):
        app.config.from_object('tests.config')
        db.session.close()
        db.drop_all() # http://docs.sqlalchemy.org/en/latest/orm/extensions/declarative/basic_use.html
        db.create_all()

        self.pay_ranges = [
            PayRange(lower=0, upper=29999.99),
            PayRange(lower=30000, upper=69999.99),
            PayRange(lower=70000, upper=99999.99)
        ]
        for pay_range in self.pay_ranges:
            db.session.add(pay_range)

        self.perks = [
            Perk('Yearly Bonus', listed=True),
            Perk('Food / Drinks', listed=True)
        ]
        for perk in self.perks:
            db.session.add(perk)

        self.employment_types = [
            EmploymentType('Full-Time', listed=True),
            EmploymentType('Part-Time', listed=True),
            EmploymentType('Independent Contractor', listed=True)
        ]
        for employment_type in self.employment_types:
            db.session.add(employment_type)

        self.roles = [
            Role('Web: Backend', listed=True),
            Role('Web: Frontend', listed=True),
            Role('Web: Full-Stack', listed=True)
        ]
        for role in self.roles:
            db.session.add(role)

        self.education_levels = [
            Education('High School'),
            Education('College / University')
        ]
        for education_level in self.education_levels:
            db.session.add(education_level)

        self.tech = [
            Tech('Python', listed=True),
            Tech('PHP', listed=True),
            Tech('Java', listed=True)
        ]
        for tech in self.tech:
            db.session.add(tech)

        db.session.commit()

    def test_create_submission(self):
        submission = Submission()
        submission.years_experience = 5
        submission.years_with_current_employer = 1
        submission.number_of_employers = 2
        submission.pay_range = self.pay_ranges[1]
        submission.perks.append(self.perks[0])
        submission.perks.append(self.perks[1])
        submission.perks[0].value = 5000
        submission.perks[1].value = 2000
        submission.employment_type = self.employment_types[0]
        submission.tech.append(self.tech[0])
        submission.tech.append(self.tech[2])
        submission.education = self.education_levels[1]
        db.session.commit()
        assert submission.pay_range == self.pay_ranges[1]
        assert self.perks[0] in submission.perks
        assert self.perks[1] in submission.perks
        assert self.perks[0].value == 5000
        assert self.perks[1].value == 2000
        assert submission.employment_type == self.employment_types[0]
        assert self.tech[0] in submission.tech
        assert self.tech[2] in submission.tech
        assert submission.education == self.education_levels[1]


if __name__ == '__main__':
    unittest.main()