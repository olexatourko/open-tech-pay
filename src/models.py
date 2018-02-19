from src import db
from sqlalchemy.orm import relationship
from datetime import datetime
from sqlalchemy.ext.associationproxy import association_proxy

class PayRange(db.Model):
    __tablename__ = 'pay_range'
    id = db.Column(db.Integer, primary_key=True)
    lower = db.Column(db.Numeric)
    upper = db.Column(db.Numeric)

    def __init__(self, lower, upper):
        assert lower < upper
        self.lower = lower
        self.upper = upper

class Role(db.Model):
    __tablename__ = 'role'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)

    def __init__(self, name):
        self.name = name

class Submission(db.Model):
    __tablename__ = 'submission'
    id = db.Column(db.Integer, primary_key=True)

    """ For confirmation and verification """
    email = db.Column('email', db.String(255))
    confirmation_code = db.Column('confirmation_code', db.String(255))
    confirmed = db.Column('confirmed', db.Boolean)
    verified = db.Column('verified', db.Boolean)

    created_at = db.Column(db.DateTime,  default=datetime.utcnow)
    updated_at = db.Column(db.DateTime,  onupdate=datetime.utcnow)

    """ Relations """
    submission_to_pay_range = relationship("SubmissionToPayRange", uselist=False, cascade="all, delete-orphan")
    submission_to_role = relationship("SubmissionToRole", cascade="all, delete-orphan")
    pay_range = association_proxy('submission_to_pay_range', 'pay_range')
    role = association_proxy('submission_to_role', 'role')

class EmailDomain(db.Model):
    __tablename__ = 'email_domain'
    id = db.Column(db.Integer, primary_key=True)
    domain = db.Column(db.Text)

""" Relation classes """

class SubmissionToPayRange(db.Model):
    __tablename__ = 'submission_to_pay_range'
    id = db.Column(db.Integer, primary_key=True)

    """
    Relations:
    
    1 Submission
    1 PayRange
    """

    submission_id = db.Column(db.Integer, db.ForeignKey('submission.id', ondelete='CASCADE'))
    pay_range_id = db.Column(db.Integer, db.ForeignKey('pay_range.id', ondelete='CASCADE'))
    submission = relationship(Submission)
    pay_range = relationship(PayRange)

class SubmissionToRole(db.Model):
    __tablename__ = 'submission_to_role'
    id = db.Column(db.Integer, primary_key=True)

    """
    Relations:

    1 Submission
    1 Role
    """

    submission_id = db.Column(db.Integer, db.ForeignKey('submission.id', ondelete='CASCADE'))
    role_id = db.Column(db.Integer, db.ForeignKey('role.id', ondelete='CASCADE'))
    submission = relationship(Submission)
    role = relationship(Role)