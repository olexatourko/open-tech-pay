import unittest
from unittest.mock import patch
from src import app, db
from src.application import submit, confirm_post
from src.models import Submission, EmploymentType, Location, Education, Tech, VerificationRequest
from utils.seeding.seed_core import seed_core
from utils.seeding.seed_preset_submissions import seed_preset_submisssions
import json

''' Test that the submission process work. This isn't quite an end-to-end test because the frontend is not tested.'''
class TestSubmit(unittest.TestCase):
    def setUp(self):
        app.config.from_object('tests.config')
        self.app = app.test_client()
        db.session.close()
        db.drop_all()  # http://docs.sqlalchemy.org/en/latest/orm/extensions/declarative/basic_use.html
        db.create_all()
        seed_core(db)
        db.session.commit()

        self.payload = {
            'payload': json.dumps({
                'salary': 50000,
                'email': 'test@company1.com',
                'years_experience': 1,
                'years_with_current_employer': 1,
                'number_of_employers': 1,
                'employment_type': EmploymentType.query.first().id,
                'location': EmploymentType.query.first().id,
                'education': EmploymentType.query.first().id,
                'perks': [],
                'roles': [
                    {
                        'id': Tech.query.first().id
                    }
                ],
                'techs': [
                    {
                        'name': 'Not already in DB'
                    }
                ]
            })
        }

    def test_submit(self):
        response = self.app.post('/submit', data=self.payload)
        self.assertEqual(response.status_code, 200)
        submission = Submission.query.filter_by(email='test@company1.com').first()
        self.assertIsNotNone(submission)

    def test_confirm(self):
        self.app.post('/submit', data=self.payload)
        submission = Submission.query.filter_by(email='test@company1.com').first()
        response = self.app.post('/confirm', data={
            'code': submission.confirmation_code
        })
        # Grab it again since the confirm endpoint closes the session
        submission = Submission.query.filter_by(email='test@company1.com').first()
        self.assertTrue(submission.confirmed)



class TestSubmitWithVerificationRequest(unittest.TestCase):
    def setUp(self):
        app.config.from_object('tests.config')
        self.app = app.test_client()
        db.session.close()
        db.drop_all()  # http://docs.sqlalchemy.org/en/latest/orm/extensions/declarative/basic_use.html
        db.create_all()
        seed_core(db)
        db.session.commit()

        self.payload = {
            'payload': json.dumps({
                'salary': 50000,
                'email': 'test@company1.com',
                'years_experience': 1,
                'years_with_current_employer': 1,
                'number_of_employers': 1,
                'employment_type': EmploymentType.query.first().id,
                'location': EmploymentType.query.first().id,
                'education': EmploymentType.query.first().id,
                'perks': [],
                'roles': [
                    {
                        'id': Tech.query.first().id
                    }
                ],
                'techs': [
                    {
                        'name': 'Not already in DB'
                    }
                ],
                'verification_request': {
                    'profile_url': 'https://www.linkedin.com/in/test',
                    'employer_name': 'Test Company',
                    'note': 'Test note'
                }
            })
        }

    def test_happy_path(self):
        response = self.app.post('/submit', data=self.payload)
        self.assertEqual(response.status_code, 200)
        submission = Submission.query.filter_by(email='test@company1.com').first()
        self.assertIsNotNone(submission.verification_request)
        self.assertIsNotNone(submission.verification_request.id)
        self.assertEqual(submission.verification_request.status, 'open')

    @patch('src.request_schemas.is_email_whitelisted')
    def test_email_already_whitelisted(self, mock_is_email_whitelisted):
        mock_is_email_whitelisted.return_value = True
        response = self.app.post('/submit', data=self.payload)
        self.assertEqual(response.status_code, 200)
        self.assertIn('errors', json.loads(response.data))
        self.assertIsNone(Submission.query.filter_by(email='test@company1.com').first())
