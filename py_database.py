from marshmallow import Schema, fields
from app import database as db

class User(db.Model): #CREATE USER TABLE
    id_user= db.Column(db.Integer, primary_key=True)
    user_name=db.Column(db.String(80), unique=True, nullable=False)
    password=db.Column(db.string(120), nullable=False)
    
    def __repr__(self) -> str:
        return f'<User: {self.user_name}>'

  
class UserSchema(Schema): #VALIDATE OUR TABLE
    username=fields.str(required=True, validate=lambda p:len(p)>0)
    password=fields.Str(required=True, validate=lambda p:len(p)>0)


def create_tables():
    db.create_all()