from flask import Flask, request, jsonify
from werkzeug.security import check_password_hash, generate_password_hash
from flask_sqlalchemy import SQLAlchemy
from marshmallow import ValidationError
from models import db, User
from schemas import UserSchema
import re

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    user_schema = UserSchema()
    
    try:
        user_schema.load(data)
    except ValidationError as e:
        return jsonify(e.messages), 400
        
    username = data.get('username')
    password = data.get('password')
    
    if not re.match(r'^[a-zA-Z0-9_]+$', username):
        return jsonify({'message': 'Username can only contain letters, numbers, and underscores.'}), 400
    
    if len(password) < 8 or not any(char.isdigit() for char in password):
        return jsonify({'message': 'Password must be at least 8 characters long and contain at least one number.'}), 400
    
    if User.query.filter_by(username=username).first():
        return jsonify({'message': f'User {username} already exists.'}), 400

    hashed_password = generate_password_hash(password, method='sha256')
    new_user = User(username=username, password=hashed_password)
    
    try:
        db.session.add(new_user)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Failed to register. Please try later.'}), 500

    return jsonify({'message': f'User {username} registered successfully!'}), 201


@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user_schema = UserSchema()
    
    try:
        user_schema.load(data)
    except ValidationError as e:
        return jsonify(e.messages), 400

    username = data.get('username')
    password = data.get('password')
    
    user = User.query.filter_by(username=username).first()
    
    if user and check_password_hash(user.password, password):
        return jsonify({'message': f'User {username} logged in successfully!'}), 200
    else:
        return jsonify({'message': 'Invalid username or password.'}), 401

if __name__ == "__main__":
    app.run(debug=True)
