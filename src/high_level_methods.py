from src import app, db
from models import *
from sqlalchemy import and_
import uuid
import re


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


def check_email(email):
    """

    :param email: It is assumed that the email has already been sanitized
    :return: dict
    """
    email_domain = re.search(r'(?<=@)[\w.]+$', email).group(0)
    submission = Submission.query.filter(and_(
        Submission.confirmed == True,
        Submission.email == email
    )).first()

    employer = Employer.query.filter(
        Employer.email_domain == email_domain
    ).first()


    return {
        'in_use': submission is not None,
        'whitelisted': employer is not None
    }


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
