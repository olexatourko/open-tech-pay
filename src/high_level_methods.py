from src import app, db
from models import *
from sqlalchemy import and_
import uuid
import re
import datetime

'''
Contains high-level application logic
'''

def get_confirmation_code():
    uid = uuid.uuid4()
    return uid.hex


def confirm_submission(confirmation_code):
    submission = Submission.query.filter(
        and_(
            Submission.confirmed == False,
            Submission.confirmation_code == confirmation_code
        )
    ).first()

    if submission:
        submission.confirmed = True
        db.session.add(submission)
        db.session.commit()

    return submission


def is_email_whitelisted(email):
    email_domain = re.search(r'(?<=@)[\w.]+$', email).group(0)
    employer = Employer.query.filter(
        Employer.email_domain == email_domain
    ).first()
    return employer is not None


def is_email_recently_used(email, date=datetime.date.today()):
    submission = Submission.query.filter(and_(
        Submission.confirmed == True,
        Submission.email == email,
        Submission.created_at >= date - datetime.timedelta(days=365)
    )).first()
    return submission is not None


def get_aggregate_data():
    from sqlalchemy.sql import func

    region_id = Location.query.filter(Location.name == app.config['REGION_NAME']).first().id
    query = db.session.query(
        func.avg(Submission.salary).label('average_salary'),
        func.avg(Submission.years_experience).label('average_experience')
    ).filter(
        Submission.confirmed == True,
        Submission.location.has(
            Location.id == region_id
        )
    )
    result = query.first()
    return {
        'average_salary': float(result[0]),
        'average_experience': float(result[1]),
    }
