from flask import request, jsonify, abort
from flask_jwt_extended import (create_access_token)
from validate_email import validate_email
from .models import User
from . import v2


@v2.route('/api/v2/auth/signup', methods = ['POST'])
def create_user():
    data = request.get_json()
    username = data.get('username')
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')

    if username is not None and username.strip() == "":
        return jsonify({"message" : "Please fill in all the fields"}), 400
    if name is not None and name.strip() == "":
        return jsonify({"message" : "Please fill in all the fields"}), 400
    if not validate_email(email):
        return jsonify({"message" : "Please enter a valid email"}), 400
    if password is not None and password.strip() == "":
        return jsonify({"message" : "Please fill in all the fields"}), 400
  
    user = User(name=name, username=username, email=email, password=password)
    user.add()
    return jsonify({"message" : "Account created successfully"}), 201
    


@v2.route('/api/v2/auth/login', methods = ['POST'])
def login():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400
    username = request.json.get('username')
    password = request.json.get('password')
    if not username:
        return jsonify({"msg": "Missing username parameter"}), 400
    if not password:
        return jsonify({"msg": "Missing password parameter"}), 400
    user = User().get_by_username(username)
    if not user:
        return jsonify({"msg":"No auth"}), 401
    if not user.check_password(password):
        return jsonify({"msg":"No auth"}), 401
    
    # Identity can be any data that is json serializable
    access_token = create_access_token(identity=user.username)
    return jsonify(access_token=access_token), 200





    