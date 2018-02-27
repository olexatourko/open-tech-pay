from src import db
from models import *
from sqlalchemy import and_
import uuid


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
