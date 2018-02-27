from src import db
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

