from flask import request, jsonify, abort 
from datetime import datetime
from dateutil import parser
from flask_jwt_extended import (create_access_token, jwt_required, get_jwt_identity)
from validate_email import validate_email
from .models import User, Ride
from . import v2
import re


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

    EMAIL_REGEX = re.compile(r"\"?([-a-zA-Z0-9.`?{}]+@\w+\.\w+)\"?")
    if not EMAIL_REGEX.match(email):
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
        return jsonify({"msg":"Invalid username or password"}), 401
    if not user.check_password(password):
        return jsonify({"msg":"Invalid username or password"}), 401
    
    # Identity can be any data that is json serializable
    access_token = create_access_token(identity=user.username)
    return jsonify(access_token=access_token), 200


@v2.route('/api/v2/rides',  methods = ['POST'])
@jwt_required
def create_ride():
    data = request.get_json()
    pickup = data.get('pickup')
    dropoff = data.get('dropoff')
    time = data.get('time')  

    username = get_jwt_identity()
    driver = User().get_by_username(username)

    if not driver:
        return jsonify({"message" : "Invalid driver"}), 400

    
    s_time = parser.parse(time)
    if s_time < datetime.now():
        return jsonify({"message":"Can't post in the past"})
    driver_rides = Ride()
    driveride = driver_rides.get_by_user(driver.id)
    if driveride:
        for ride in driveride:
            
            diff = s_time - ride.time
            if diff.seconds < 18000:
                return jsonify({"message":"Cannot post another ride"})

    


    if pickup is not None and pickup.strip() == "":
        return jsonify({"message" : "Please fill in all the fields"}), 400
    if dropoff is not None and dropoff.strip() == "":
        return jsonify({"message" : "Please fill in all the fields"}), 400
    if time is not None and time.strip() == "":
        return jsonify({"message" : "Please fill in all the fields"}), 400

    ride = Ride(pickup = pickup , dropoff = dropoff,  time=time)
    ride.add(driver.id)
    return jsonify({
                "message" : "Ride created successfully"}), 201


@v2.route('/api/v2/rides')
@jwt_required
def get_rides():
    trip = Ride()
    
    return jsonify({
        'rides':
         [ride.serialize() for ride in trip.get_all()]})


@v2.route('/api/v2/ride/<int:id>', methods = ['GET'])
@jwt_required
def get_ride(id):
    trip = Ride()
    ride =  trip.get_one(id)

    if not ride:
        return jsonify({"message": "Ride does not exist"}), 404

    return jsonify({'ride': ride.serialize()})


@v2.route('/api/v2/ride/<int:id>',  methods = ['PUT'])
@jwt_required
def update_ride(id):
    data = request.get_json()
    pickup = data.get('pickup', None)
    dropoff = data.get('dropoff', None)
    time = data.get('time', None)
    ride = Ride().get_one(id)
    if not ride:
        return jsonify({"message": "Ride does not exist"}), 404
    
    if pickup:
        ride.pickup = pickup
    if dropoff:
        ride.dropoff = dropoff
    if time:
        ride.time = time

    
    
    ride.update()
    return (jsonify({
                "message" : "Ride updated successfully"}), 202)


@v2.route('/api/v2/ride/<int:id>',  methods = ['DELETE'])
@jwt_required
def delete_ride(id):
    r = Ride().get_one(id)
    if r:
        r.delete(id)
        return (jsonify({"message" : "Ride deleted successfully"}), 200)
    return (jsonify({"message" : "Ride delete failed"}), 400)





    