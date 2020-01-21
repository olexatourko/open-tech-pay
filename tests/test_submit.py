import unittest
from src import app, db
from src.application import submit, confirm_post
from src.models import Submission, EmploymentType, Location, Education, Tech
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
