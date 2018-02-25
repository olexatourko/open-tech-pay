from models import *
from marshmallow import Schema, fields, post_load


def dump_dict_values(class_instance, raw_dict):
    for key, value in raw_dict.items():
        if hasattr(class_instance, key): setattr(class_instance, key, value)


class PayRangeSchema(Schema):
    id = fields.Integer()
    lower = fields.Number()
    upper = fields.Number()


class PerkSchema(Schema):
    id = fields.Integer()
    name = fields.String()
    description = fields.String()
    listed = fields.Boolean()

    @post_load
    def make_mode(self, data):
        model = Perk()
        dump_dict_values(model, data)
        return model


class EmploymentTypeSchema(Schema):
    id = fields.Integer()
    name = fields.String()


class RoleSchema(Schema):
    id = fields.Integer()
    name = fields.String()
    listed = fields.Boolean()

    @post_load
    def make_mode(self, data):
        model = Role()
        dump_dict_values(model, data)
        return model


class EducationSchema(Schema):
    id = fields.Integer()
    name = fields.String()


class TechSchema(Schema):
    id = fields.Integer()
    name = fields.String()

    @post_load
    def make_mode(self, data):
        model = Tech()
        dump_dict_values(model, data)
        return model


class EmailDomainSchema(Schema):
    id = fields.Integer()
    domain = fields.String()


class SubmissionSchema(Schema):
    id = fields.Integer()
    years_experience = fields.Integer()
    number_of_employers = fields.Integer()
    years_with_current_employer = fields.Integer()

    pay_range = fields.Nested('PayRangeSchema')
    perks = fields.Nested('PerkSchema', many=True)
    employment_type = fields.Nested('EmploymentTypeSchema')
    roles = fields.Nested('RoleSchema', many=True)
    education = fields.Nested('EducationSchema')
    tech = fields.Nested('TechSchema', many=True)