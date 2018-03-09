from marshmallow import Schema, fields, post_load, validates, validates_schema, ValidationError
from marshmallow.validate import *
from src.models import *


class SubmissionRequestSchema(Schema):
    """
    This class ONLY validates the inputs. It does not fetch the models.
    """
    def validate_pay_range(value):
        pay_range = PayRange.query.filter(PayRange.id == value).first()
        if not pay_range:
            raise ValidationError('Pay Range does not exist.')

    def validate_employment_type(value):
        employment_type = EmploymentType.query.filter(EmploymentType.id == value).first()
        if not employment_type:
            raise ValidationError('Pay Range does not exist.')

    def validate_education(value):
        education = Education.query.filter(Education.id == value).first()
        if not education:
            raise ValidationError('Education does not exist.')

    def validate_email(value):
        submission = Submission.query.filter(
            Submission.email == value
        ).first()

        if submission and submission.confirmed:
            raise ValidationError('Submission for this email already exists')

    email = fields.Email(required=True, validate=validate_email)
    years_experience = fields.Integer(required=True)
    years_with_current_employer = fields.Integer(required=True)
    number_of_employers = fields.Integer()

    pay_range = fields.Integer(required=True, validate=validate_pay_range)
    employment_type = fields.Integer(required=True, validate=validate_employment_type)
    education = fields.Integer(required=True, validate=validate_education)

    perks = fields.List(fields.Dict(), validate=Length(max=10))
    roles = fields.List(fields.Dict(), required=True, validate=Length(min=1, max=5))
    techs = fields.List(fields.Dict(), validate=Length(max=15))

    @validates_schema(skip_on_field_errors=True)
    def validate_object(self, data):
        """ years_experience >= years_with_current_employer """
        if 'years_with_current_employer' in data and 'years_experience' in data:
            if not data['years_with_current_employer'] <= data['years_experience']:
                raise ValidationError('Years with current employer must be <= total years of experience',
                      ['years_with_current_employer', 'years_experience'])


class ConfirmRequestSchema(Schema):
    confirmation_code = fields.String(required=True)


class CheckEmailRequestSchema(Schema):
    email = fields.Email(required=True)