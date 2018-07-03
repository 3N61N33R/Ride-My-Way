from flask import request, jsonify, make_response, abort
import json 
from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity, create_access_token

)
from .models import User, Ride, Request, rides, requests
from . import v2


@v2.route('/api/v2/users', methods = ['POST'])
def create_user():
    data = request.get_json()
    username = data.get('username')
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')
    if username is not None and email is not None and name is not None and password is not None:
        user = User(name=name, username=username, email=email, password=password)
        user.add()
        return jsonify({
                "message" : "Account created successfully"}), 201
    else:
        return jsonify({
                "message" : "Please fill in all the fields"}), 201
    
@v2.route('/api/v2/login', methods = ['POST'])
def login():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400
    username = request.json.get('username', None)
    password = request.json.get('password', None)
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


@v2.route('/api/v2/rides',  methods = ['POST'])
@jwt_required
def create_ride():
    data = request.get_json()
    pickup = data.get('pickup')
    dropoff = data.get('dropoff')
    time = data.get('time')  

    if pickup is not None and dropoff is not None and time is not None:
        username = get_jwt_identity()
        driver = User().get_by_username(username)
        if not driver:
            return jsonify({}), 401
        # TODO -- auth 
        ride = Ride(driver = driver, pickup = pickup , dropoff = dropoff,  time=time)
        ride.add()

        return jsonify({
                "message" : "Ride created successfully"}), 201

    else:
        return jsonify({
                "message" : "Please fill in all the fields"}), 201




@v2.route('/api/v2/rides')
def get_rides():
    trip = Ride()
    rides =  trip.get_all()

    return jsonify({'rides': [ride.serialize() for ride in rides]})


@v2.route('/api/v2/ride/<int:id>', methods = ['GET'])
def get_ride(id):
    trip = Ride()
    ride =  trip.get_one(id)

    if not ride:
        return jsonify({"message": "Ride does not exist"}), 404

    return jsonify({'ride': ride.serialize()})


@v2.route('/api/v2/ride/<int:id>',  methods = ['PUT'])
def update_ride(id):
    data = request.get_json()
    pickup = data.get('pickup', None)
    dropoff = data.get('dropoff', None)
    time = data.get('time', None)
    ride = Ride().get_one(id)
    if not ride:
        return abort(404)
    
    if pickup:
        ride.pickup = pickup
    if dropoff:
        ride.dropoff = dropoff
    if time:
        ride.time = time
    ride.update()
    return (jsonify({
                "message" : "Ride updated successfully"}), 201)


@v2.route('/api/v2/ride/<int:id>',  methods = ['DELETE'])
def delete_ride(id):
    r = Ride().get_one(id)
    if r:
        r.delete(id)
        return (jsonify({
                "message" : "Ride deleted successfully"}), 200)
    return abort(404)


""" endpoints for requests"""

@v2.route('/api/v2/ride/<int:id>/request',  methods = ['POST'])
@jwt_required
def create_request(id):
    ride = Ride().get_one(id)
    
    username = get_jwt_identity()
    user = User().get_by_username(username)
    
    if not ride:
        return abort(404)

    req = Request(user = user, ride=ride)
    req.add()

    return (jsonify({
                "message" : "Request made successfully"}), 201)  


@v2.route('/api/v2/ride/<int:id>/requests')
def get_requests(id):
    query = Request()
    requests = query.get_all_requests(id)

    return jsonify({'requests': [request.serialize() for request in requests]})


@v2.route('/api/v2/ride/<int:ride_id>/request/<int:request_id>')
def get_request(ride_id, request_id):
    query = Request()
    request = query.get_one_request(ride_id, request_id)
    if not request:
        return abort(404)

    return jsonify({'request': request.serialize()})


@v2.route('/api/v2/ride/<int:ride_id>/request/<int:request_id>',  methods = ['DELETE'])
def delete_request(ride_id, request_id):
    query = Request()
    request = query.get_one_request(ride_id, request_id)
    if not request:
        return abort(404)
    requests.remove(request)

    return (jsonify({
                "message" : "Request deleted successfully"}), 200)



    