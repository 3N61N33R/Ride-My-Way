from flask import request, jsonify, make_response, abort
import json 
from .models import User, Ride, Request, rides, requests
from . import app


@app.route('/api/v1/users', methods = ['POST'])
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
    

@app.route('/api/v1/rides',  methods = ['POST'])
def create_ride():
    data = request.get_json()
    name = data.get('name')
    pickup = data.get('pickup')
    dropoff = data.get('dropoff')
    time = data.get('time')  

    if name is not None and pickup is not None and dropoff is not None and time is not None:


        ride = Ride( name = name, pickup = pickup , dropoff = dropoff,  time=time)
        ride.add()

        return jsonify({
                "message" : "Ride created successfully"}), 201

    else:
        return jsonify({
                "message" : "Please fill in all the fields"}), 201




@app.route('/api/v1/rides')
def get_rides():
    trip = Ride()
    rides =  trip.get_all()

    return jsonify({'rides': rides})


@app.route('/api/v1/ride/<int:id>', methods = ['GET'])
def get_ride(id):
    trip = Ride()
    ride =  trip.get_one(id)

    if not ride:
        return jsonify({"message": "Ride does not exist"}), 404

    return jsonify({'ride': ride.serialize()})


@app.route('/api/v1/ride/<int:id>',  methods = ['PUT'])
def update_ride(id):
    data = request.get_json()
    pickup = data.get('pickup', None)
    dropoff = data.get('dropoff', None)
    time = data.get('time', None)
    ride = Ride().get_one(id)
    if not ride:
        return abort(404)
    index = rides.index(ride)
    
    if pickup:
        rides[index].pickup = pickup
    if dropoff:
        rides[index].dropoff = dropoff
    if time:
        rides[index].time = time

    return (jsonify({
                "message" : "Ride updated successfully"}), 201)


@app.route('/api/v1/ride/<int:id>',  methods = ['DELETE'])
def delete_ride(id):
    r = Ride()
    if r.delete(id):
        return (jsonify({
                "message" : "Ride deleted successfully"}), 200)
    return abort(404)


""" endpoints for requests"""

@app.route('/api/v1/ride/<int:id>/request',  methods = ['POST'])
def create_request(id):
    data = request.get_json()
    name = data['name']
    ride = Ride().get_one(id)
    
    if not ride:
        return abort(404)

    req = Request(name = name, ride=ride)
    req.add()

    return (jsonify({
                "message" : "Request made successfully"}), 201)  


@app.route('/api/v1/ride/<int:id>/requests')
def get_requests(id):
    query = Request()
    requests = query.get_all_requests(id)

    return jsonify({'requests': requests})


@app.route('/api/v1/ride/<int:ride_id>/request/<int:request_id>')
def get_request(ride_id, request_id):
    query = Request()
    request = query.get_one_request(ride_id, request_id)
    if not request:
        return abort(404)

    return jsonify({'request': request.serialize()})


@app.route('/api/v1/ride/<int:ride_id>/request/<int:request_id>',  methods = ['DELETE'])
def delete_request(ride_id, request_id):
    query = Request()
    request = query.get_one_request(ride_id, request_id)
    if not request:
        return abort(404)
    requests.remove(request)

    return (jsonify({
                "message" : "Request deleted successfully"}), 200)



    