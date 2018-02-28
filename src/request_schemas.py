from marshmallow import Schema, fields, post_load, validates, validates_schema, ValidationError

class ConfirmSchema(Schema):
    confirmation_code = fields.String(required=True)

class CheckEmailSchema(Schema):
    email = fields.Email(required=True)