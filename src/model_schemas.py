from models import *
from marshmallow import Schema, fields, post_load, validates, validates_schema, ValidationError


def dump_dict_values(class_instance, raw_dict):
    for key, value in raw_dict.items():
        if hasattr(class_instance, key): setattr(class_instance, key, value)


class PerkSchema(Schema):
    id = fields.Integer()
    name = fields.String(required=True)
    description = fields.String()
    listed = fields.Boolean()

    @post_load
    def make_model(self, data):
        model = Perk()
        dump_dict_values(model, data)
        return model


class EmploymentTypeSchema(Schema):
    id = fields.Integer()
    name = fields.String(required=True)


class RoleSchema(Schema):
    id = fields.Integer()
    name = fields.String(required=True)
    listed = fields.Boolean()

    @post_load
    def make_model(self, data):
        model = Role()
        dump_dict_values(model, data)
        return model


class EducationSchema(Schema):
    id = fields.Integer()
    name = fields.String(required=True)


class TechSchema(Schema):
    id = fields.Integer()
    name = fields.String(required=True)

    @post_load
    def make_model(self, data):
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
    perks = fields.Nested('PerkSchema', many=True)
    employment_type = fields.Nested('EmploymentTypeSchema')
    roles = fields.Nested('RoleSchema', many=True)
    education = fields.Nested('EducationSchema')
    techs = fields.Nested('TechSchema', many=True)

    @post_load
    def make_model(self, data):
        if 'instance' in data:
            model = data['instance']
        else:
            model = Submission()

        dump_dict_values(model, data)
        return model

    @validates_schema(skip_on_field_errors=True)
    def validate_object(self, data):
        if not ('years_with_current_employer' in data and 'years_experience') in data:
            return

        if not data['years_with_current_employer'] <= data['years_experience']:
            raise ValidationError('Years with current employer must be <= total years of experience',
                  ['years_with_current_employer', 'years_experience'])


