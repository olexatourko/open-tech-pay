from src.models import *
from marshmallow import Schema, fields, post_load, validates, validates_schema, ValidationError
from marshmallow.validate import Length


'''
Contains logic to convert models to dicts and vice-versa using Marshmallow
'''


def dump_dict_values(class_instance, raw_dict):
    for key, value in raw_dict.items():
        if hasattr(class_instance, key): setattr(class_instance, key, value)


class PerkSchema(Schema):
    id = fields.Integer()
    name = fields.String(required=True, validate=Length(min=1, max=32,
        error="Perk name must be between {min} and {max} characters."))
    description = fields.String()
    listed = fields.Boolean()

    @post_load
    def make_model(self, data, **kwargs):
        model = Perk()
        dump_dict_values(model, data)
        return model


class SubmissionToPerkSchema(Schema):
    submission_id = fields.Integer()
    perk_id = fields.Integer()
    perk = fields.Nested('PerkSchema')
    value = fields.Number()


class EmploymentTypeSchema(Schema):
    id = fields.Integer()
    name = fields.String(required=True)


class RoleSchema(Schema):
    id = fields.Integer()
    name = fields.String(required=True, validate=Length(min=1, max=32,
        error="Role name must be between {min} and {max} characters."))
    listed = fields.Boolean()

    @post_load
    def make_model(self, data, **kwargs):
        model = Role()
        dump_dict_values(model, data)
        return model


class EducationSchema(Schema):
    id = fields.Integer()
    name = fields.String(required=True)


class LocationSchema(Schema):
    id = fields.Integer()
    name = fields.String(required=True)


class TechSchema(Schema):
    id = fields.Integer()
    name = fields.String(required=True, validate=Length(min=1, max=32,
        error="Technology name must be between {min} and {max} characters."))
    listed = fields.Boolean()

    @post_load
    def make_model(self, data, **kwargs):
        model = Tech()
        dump_dict_values(model, data)
        return model


class EmployerSchema(Schema):
    id = fields.Integer()
    name = fields.String(required=True)
    email_domain = fields.String(required=True)
    url = fields.String(required=True)


class SubmissionSchema(Schema):
    id = fields.Integer()
    salary = fields.Number(required=True)
    email = fields.Email(required=True)
    years_experience = fields.Integer(required=True)
    number_of_employers = fields.Integer()
    years_with_current_employer = fields.Integer()
    verified = fields.Boolean()
    perks = fields.Nested('PerkSchema', many=True)
    submission_to_perks = fields.Nested('SubmissionToPerkSchema',
        exclude=('submission_id', 'perk_id'),
        many=True)
    employment_type = fields.Nested('EmploymentTypeSchema')
    location = fields.Nested('LocationSchema')
    roles = fields.Nested('RoleSchema', exclude=('id', 'listed'), many=True)
    education = fields.Nested('EducationSchema', exclude=('id',))
    techs = fields.Nested('TechSchema', exclude=('id', 'listed'), many=True)
    created_at = fields.DateTime()

    @post_load
    def make_model(self, data, **kwargs):
        if 'instance' in data:
            model = data['instance']
        else:
            model = Submission()

        dump_dict_values(model, data)
        return model

    @validates_schema(skip_on_field_errors=True)
    def validate_object(self, data, **kwargs):
        if not ('years_with_current_employer' in data and 'years_experience') in data:
            return

        if not data['years_with_current_employer'] <= data['years_experience']:
            raise ValidationError(
                {
                    'years_with_current_employer': 'Years with current employer must be <= total years of experience',
                    'years_experience': 'years_with_current_employer'
                }
            )
