from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash
from py_database import create_tables, User, UserSchema
from marshmallow import Schema, fields, ValidationError


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
    passwd = data.get['password']
    
    if User.query.filter_by(username=username).first():
        return jsonify({'message': f'User {username} already exists. '}), 400

    hashed_password = generate_password_hash(passwd, method='sha256')
    new_user=User(username, hashed_password)
    database.session.add(new_user)
    database.commit()
    
    
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
    