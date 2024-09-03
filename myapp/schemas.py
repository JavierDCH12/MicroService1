from marshmallow import Schema, fields

class UserSchema(Schema):  
    username = fields.Str(required=True, validate=lambda p: len(p) > 0)
    password = fields.Str(required=True, validate=lambda p: len(p) >= 8)
