#!/usr/bin/python
# -*- coding: utf-8 -*-

import unittest

from src import app
from src.high_level_methods import *
from utils.seeding.seed_core import seed_core
from utils.seeding.seed_preset_submissions import seed_preset_submisssions
import datetime


class TestHighLevelMethods(unittest.TestCase):

    def setUp(self):
        app.config.from_object('tests.config')
        db.session.close()
        db.drop_all()  # http://docs.sqlalchemy.org/en/latest/orm/extensions/declarative/basic_use.html
        db.create_all()
        seed_core(db)
        seed_preset_submisssions(db)
        db.session.add(Employer(name='Company 1', email_domain='company1.com', url='https://company1.com'))
        db.session.commit()
        self.submissions = Submission.query.all()

    def test_is_email_whitelisted(self):
        assert is_email_whitelisted('test@company1.com') is True
        assert is_email_whitelisted('test@unlisted.com') is False

    def test_is_email_recently_used(self):
        self.submissions[0].email = 'test@company1.com'
        self.submissions[0].confirmed = True
        self.submissions[1].email = 'test@company2.com'
        self.submissions[1].confirmed = False
        db.session.commit()

        assert is_email_recently_used('test@company1.com', date=datetime.date(2017, 1, 1)) is True
        assert is_email_recently_used('test@company2.com', date=datetime.date(2017, 1, 1)) is False
        # Should be False since its been > 1 year since last submission
        assert is_email_recently_used('test@company1.com', date=datetime.date(2020, 1, 1)) is False

    def test_confirm_submission(self):
        self.submissions[0].confirmed = False
        self.submissions[0].confirmation_code = '123abc'

        assert confirm_submission('456def') is None
        assert confirm_submission('123abc') is not None
        assert confirm_submission('123abc') is None

    def test_get_aggregate_data(self):
        self.submissions[0].salary = 40000
        self.submissions[0].years_experience = 1
        self.submissions[1].salary = 50000
        self.submissions[1].years_experience = 2
        self.submissions[2].salary = 60000
        self.submissions[2].years_experience = 3
        result = get_aggregate_data()
        assert result['average_salary'] == 50000
        assert result['average_experience'] == 2

        Submission.query.delete()
        result = get_aggregate_data()
        assert result['average_salary'] == 'NA'
        assert result['average_experience'] == 'NA'

if __name__ == '__main__':
    unittest.main()