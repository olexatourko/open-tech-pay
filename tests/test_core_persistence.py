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

        self.perks = [
            Perk('Yearly Bonus', listed=True),
            Perk('Food / Drinks', listed=True)
        ]
        for perk in self.perks:
            db.session.add(perk)

        self.locations = [
            Location('London, Ontario'),
            Location('Near London, Ontario')
        ]
        for location in self.locations:
            db.session.add(location)

        self.employment_types = [
            EmploymentType('Full-Time'),
            EmploymentType('Part-Time'),
            EmploymentType('Independent Contractor')
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

        self.techs = [
            Tech('Python', listed=True),
            Tech('PHP', listed=True),
            Tech('Java', listed=True)
        ]
        for tech in self.techs:
            db.session.add(tech)

        db.session.commit()

    def test_create_submission(self):
        submission = Submission()
        submission.salary = 60000
        submission.years_experience = 5
        submission.years_with_current_employer = 1
        submission.number_of_employers = 2
        submission.perks.append(self.perks[0])
        submission.submission_to_perks.append(SubmissionToPerk(self.perks[1], value=100))

        submission.employment_type = self.employment_types[0]
        submission.location = self.locations[0]
        submission.techs.append(self.techs[0])
        submission.techs.append(self.techs[2])
        submission.education = self.education_levels[1]
        db.session.add(submission)
        db.session.commit()

        submission = Submission.query.first()
        assert submission.salary == 60000
        assert self.perks[0] in submission.perks
        assert self.perks[1] in submission.perks
        assert submission.submission_to_perks[1].value == 100
        assert submission.employment_type == self.employment_types[0]
        assert submission.location == self.locations[0]
        assert self.techs[0] in submission.techs
        assert self.techs[2] in submission.techs
        assert submission.education == self.education_levels[1]


if __name__ == '__main__':
    unittest.main()