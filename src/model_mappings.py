from models import *
from marshmallow import Schema, fields

class PayRangeSchema(Schema):
    id = fields.Integer()
    lower = fields.Number()
    upper = fields.Number()

class PerkSchema(Schema):
    id = fields.Integer()
    name = fields.String()
    description = fields.String()
    listed = fields.Boolean()

class EmploymentTypeSchema(Schema):
    id = fields.Integer()
    name = fields.String()

class RoleSchema(Schema):
    id = fields.Integer()
    name = fields.String()
    listed = fields.Boolean()

class EducationSchema(Schema):
    id = fields.Integer()
    name = fields.String()

class TechSchema(Schema):
    id = fields.Integer()
    name = fields.String()

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