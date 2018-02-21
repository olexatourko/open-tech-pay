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

class Perk(db.Model):
    __tablename__ = 'perk'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    description = db.Column(db.Text)
    listed = db.Column('listed', db.Boolean)

    def __init__(self, name, description=None, listed=False):
        self.name = name
        self.description = description
        self.listed = listed

class EmploymentType(db.Model):
    __tablename__ = 'employment_type'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)

    def __init__(self, name):
        self.name = name

class Role(db.Model):
    __tablename__ = 'role'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    listed = db.Column('listed', db.Boolean)

    def __init__(self, name, listed=False):
        self.name = name
        self.listed = listed

class Education(db.Model):
    __tablename__ = 'education'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)

    def __init__(self, name):
        self.name = name

class Tech(db.Model):
    __tablename__ = 'tech'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    listed = db.Column('listed', db.Boolean)

    def __init__(self, name, listed=False):
        self.name = name
        self.listed = listed

class Submission(db.Model):
    __tablename__ = 'submission'
    id = db.Column(db.Integer, primary_key=True)
    years_experience = db.Column(db.Integer)
    years_with_current_employer = db.Column(db.Integer)
    number_of_employers = db.Column(db.Integer)

    """ For confirmation and verification """
    email = db.Column('email', db.String(255))
    confirmation_code = db.Column('confirmation_code', db.String(255))
    confirmed = db.Column('confirmed', db.Boolean)
    verified = db.Column('verified', db.Boolean)

    created_at = db.Column(db.DateTime,  default=datetime.utcnow)
    updated_at = db.Column(db.DateTime,  onupdate=datetime.utcnow)

    """ Relations """
    submission_to_pay_range = relationship("SubmissionToPayRange", uselist=False, cascade="all, delete-orphan")
    submission_to_perk = relationship("SubmissionToPerk", cascade="all, delete-orphan")
    submission_to_employment_type = relationship("SubmissionToEmploymentType", uselist=False, cascade="all, delete-orphan")
    submission_to_role = relationship("SubmissionToRole", cascade="all, delete-orphan")
    submission_to_education = relationship("SubmissionToEducation", uselist=False, cascade="all, delete-orphan")
    submission_to_tech = relationship("SubmissionToTech", cascade="all, delete-orphan")
    pay_range = association_proxy('submission_to_pay_range', 'pay_range')
    perks = association_proxy('submission_to_perk', 'perk')
    employment_type = association_proxy('submission_to_employment_type', 'employment_type')
    roles = association_proxy('submission_to_role', 'role')
    education = association_proxy('submission_to_education', 'education')
    tech = association_proxy('submission_to_tech', 'tech')

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

    def __init__(self, pay_range):
        self.pay_range = pay_range

class SubmissionToPerk(db.Model):
    __tablename__ = 'submission_to_perk'
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Numeric)

    """
    Relations:

    1 Submission
    1 Perk
    """

    submission_id = db.Column(db.Integer, db.ForeignKey('submission.id', ondelete='CASCADE'))
    perk_id = db.Column(db.Integer, db.ForeignKey('perk.id', ondelete='CASCADE'))
    submission = relationship(Submission)
    perk = relationship(Perk)

    def __init__(self, perk, value=None):
        self.perk = perk
        self.value = value

class SubmissionToEmploymentType(db.Model):
    __tablename__ = 'submission_to_employment_type'
    id = db.Column(db.Integer, primary_key=True)

    """
    Relations:

    1 Submission
    1 EmploymentType
    """

    submission_id = db.Column(db.Integer, db.ForeignKey('submission.id', ondelete='CASCADE'))
    employment_type_id = db.Column(db.Integer, db.ForeignKey('employment_type.id', ondelete='CASCADE'))
    submission = relationship(Submission)
    employment_type = relationship(EmploymentType)

    def __init__(self, employment_type):
        self.employment_type = employment_type

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

    def __init__(self, role):
        self.role = role

class SubmissionToEducation(db.Model):
    __tablename__ = 'submission_to_education'
    id = db.Column(db.Integer, primary_key=True)

    """
    Relations:

    1 Submission
    1 Education
    """

    submission_id = db.Column(db.Integer, db.ForeignKey('submission.id', ondelete='CASCADE'))
    education_id = db.Column(db.Integer, db.ForeignKey('education.id', ondelete='CASCADE'))
    submission = relationship(Submission)
    education = relationship(Education)

    def __init__(self, education):
        self.education = education

class SubmissionToTech(db.Model):
    __tablename__ = 'submission_to_tech'
    id = db.Column(db.Integer, primary_key=True)

    """
    Relations:

    1 Submission
    1 Tech
    """

    submission_id = db.Column(db.Integer, db.ForeignKey('submission.id', ondelete='CASCADE'))
    tech_id = db.Column(db.Integer, db.ForeignKey('tech.id', ondelete='CASCADE'))
    submission = relationship(Submission)
    tech = relationship(Tech)

    def __init__(self, tech):
        self.tech = tech