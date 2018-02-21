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