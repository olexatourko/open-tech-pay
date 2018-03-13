#!/usr/bin/python
# -*- coding: utf-8 -*-

import unittest

from src import app
from src.high_level_methods import *
from utils.seeding.seed_core import seed_core
from utils.seeding.seed_random_submissions import seed_random_submisssions


class TestHighLevelMethods(unittest.TestCase):

    def setUp(self):
        app.config.from_object('tests.config')
        db.session.close()
        db.drop_all()  # http://docs.sqlalchemy.org/en/latest/orm/extensions/declarative/basic_use.html
        db.create_all()
        seed_core(db)
        seed_random_submisssions(db)
        db.session.add(Employer(name='Company 1', email_domain='company1.com', url='https://company1.com'))
        db.session.commit()
        self.submissions = Submission.query.all()

    def test_check_email(self):
        self.submissions[0].email = 'test1@company1.com'
        self.submissions[0].confirmed = True
        self.submissions[1].email = 'test2@company1.com'
        self.submissions[1].confirmed = False
        self.submissions[2].email = 'test@unlisted_company.com'
        self.submissions[2].confirmed = False
        db.session.commit()

        check_1 = check_email('test1@company1.com')
        assert check_1['in_use'] is True
        assert check_1['whitelisted'] is True

        check_2 = check_email('test2@company1.com')
        assert check_2['in_use'] is False
        assert check_2['whitelisted'] is True

        check_3 = check_email('test@unlisted_company.com')
        assert check_3['in_use'] is False
        assert check_3['whitelisted'] is False

    def test_confirm_submission(self):
        self.submissions[0].confirmed = False
        self.submissions[0].confirmation_code = '123abc'

        assert confirm_submission('456def') is None
        assert confirm_submission('123abc') is not None
        assert confirm_submission('123abc') is None

if __name__ == '__main__':
    unittest.main()