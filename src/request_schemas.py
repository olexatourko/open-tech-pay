from marshmallow import Schema, fields, post_load, validates, validates_schema, ValidationError
from marshmallow.validate import *
from src.models import *
from src.high_level_methods import is_email_recently_used, is_email_whitelisted

class SubmissionRequestSchema(Schema):
    """
    This class ONLY validates the inputs. It does not fetch the models.
    """
    def validate_employment_type(value):
        employment_type = EmploymentType.query.filter(EmploymentType.id == value).first()
        if not employment_type:
            raise ValidationError('Pay Range does not exist.')

    def validate_education(value):
        education = Education.query.filter(Education.id == value).first()
        if not education:
            raise ValidationError('Education does not exist.')

    def validate_location(value):
        location = Location.query.filter(Location.id == value).first()
        if not location:
            raise ValidationError('Location does not exist.')

    def validate_email(value):
        if is_email_recently_used(value):
            raise ValidationError('Recent submission for this email already exists.')

    salary = fields.Number(required=True, validate=Range(min=0, max=1000000))
    email = fields.Email(required=True, validate=validate_email)
    years_experience = fields.Integer(required=True)
    years_with_current_employer = fields.Integer()
    number_of_employers = fields.Integer()

    employment_type = fields.Integer(required=True, validate=validate_employment_type)
    location = fields.Integer(required=True, validate=validate_location)
    education = fields.Integer(required=True, validate=validate_education)

    perks = fields.List(fields.Dict(), validate=Length(
        max=10, error="A maximum of 10 perks are allowed. Please narrow down your selection to the most important ones."))
    roles = fields.List(fields.Dict(), required=True, validate=Length(
        min=1, max=5, error="Between 1 and 5 Roles must be selected. Please narrow down your selection to the most"
                            " important ones if you have more than 5."
    ))
    techs = fields.List(fields.Dict(), validate=Length(
        max=15, error="A maximum of 15 technologies are allowed. Please narrow down your selection to the most important ones."))

    verification_request = fields.Nested('VerificationRequestSchema', exclude=('id',))

    @validates_schema(skip_on_field_errors=True)
    def validate_object(self, data, **kwargs):
        """ years_experience >= years_with_current_employer """
        if 'years_with_current_employer' in data and 'years_experience' in data:
            if not data['years_with_current_employer'] <= data['years_experience']:
                raise ValidationError(
                    {
                        'years_with_current_employer': 'Years with current employer must be <= total years of experience',
                        'years_experience': 'Years with current employer must be <= total years of experience'
                    }
                )

        """ Detect emails with '+' in them """
        if re.search(r'.*\+.*(?=@)', data['email']):
            raise ValidationError('Invalid email', 'email')

        """ Detect emails from blacklisted domains """
        blacklisted_domains = ['mailinator.com', 'maildrop.cc']
        for domain in blacklisted_domains:
            if re.search(r'{}$'.format(domain), data['email']):
                raise ValidationError('Invalid email', 'email')

        if re.search(r'.*\+.*(?=@)', data['email']):
            raise ValidationError('Invalid email', 'email')

        """ Detect verification requests on whitelisted email """
        if 'verification_request' in data and is_email_whitelisted(data['email']):
            raise ValidationError('Manual verification request for already whitelisted email', 'email')


class ConfirmRequestSchema(Schema):
    code = fields.String(required=True)


class CheckEmailRequestSchema(Schema):
    email = fields.Email(required=True)


class FetchSubmissionsRequestSchema(Schema):
    min_experience = fields.Integer(validate=Range(min=0))
    max_experience = fields.Integer()
    locations = fields.List(fields.Integer())
    roles = fields.List(fields.Integer())
