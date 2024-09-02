from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash
from py_database import User, UserSchema
from marshmallow import ValidationError, IntegrityError
import re


app =Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
database=SQLAlchemy(app)


#REGISTER
@app.route('/register', methods=['POST'])
def register():
    
    
    data=request.json
    user_schema=UserSchema()
    
    try:
        
        user_schema.load(data)
        
    except ValidationError as e:
        return jsonify(e.messages), 400 #BadRequest and Error messages printed
        
        
    username = data.get['username']
    password = data.get['password']
    
    #VALIDATION
    if not re.match(r'^[a-zA-Z0-9_]+$', username):
        return jsonify({'message' : 'Username can only contain letters, numbers, and underscores.'}), 400
    
    if len(password) <8 or not any (char.isdigit()for char in password):
        return jsonify({'message' : 'Password must be at least 8 characters long and contain at least one number.'}), 400
    
    if User.query.filter_by(username=username).first():
        return jsonify({'message': f'User {username} already exists. '}), 400

    hashed_password = generate_password_hash(password, method='sha256')
    new_user=User(username, hashed_password)
    
    try:
        database.session.add(new_user)
        database.commit()
    except IntegrityError:
        database.session.rollback()
        return jsonify({'message': 'Failed to register. Please try later'}), 500



    
    
    return jsonify({'message':f'User {username} registered in successfully! '}), 201 #CREATED CODE 


#LOGIN
@app.route('/login', methods=['POST'])
def login():
    
    data=request.get_json()
    user_schema=UserSchema()
    
    try:
        
        user_schema.load(data)
    
    except ValidationError as e:
        return jsonify(e.messages), 400

    username = data.get['username']
    password = data.get['password']
    
    user = User.query.filter_by(username=username).first()
    
    if user and check_password_hash(user.password, password):
        return jsonify({'message': f'User {username} logged successfully! '})
    else:
        return jsonify({'message':'Invalid username or password'}), 401
    
    
    
    return jsonify({'message' : f'User {username} logged in successfully! '}), 200 #SUCCESS CODE




#RUN APP
if __name__=="__main__":
    app.run(debug=True)
    