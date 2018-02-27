from marshmallow import Schema, fields, post_load, validates, validates_schema, ValidationError

class CheckEmailSchema(Schema):
    email = fields.Email(required=True)