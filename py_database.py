from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from marshmallow import Schema, fields, ValidationError
from app import database as db

class User(db.Model): #CREATE USER TABLE
    id_user= db.Column(db.Integer, primary_key=True)
    user=db.Column(db.String(80), unique=True, nullable=False)
    password=db.Column(db.string(120), unique=True, nullable=False)

  
class UserSchema(Schema): #VALIDATE OUR TABLE
    username=fields.str(required=True, validate=lambda p:len(p)>0)
    password=fields.Str(required=True, validate=lambda p:len(p)>0)


def create_tables():
    db.create_all()