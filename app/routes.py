from flask import request, jsonify, make_response, abort
import json 
from validate_email import validate_email
from .models import User, Ride, Request, rides, requests
from . import app


@app.route('/api/v1/users', methods = ['POST'])
def create_user():
    data = request.get_json()
    username = data.get('username')
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')
    
    
    if not all([username,name,email,password]):
        return jsonify({"message" : "Please fill in all the fields"}), 400
    if not validate_email(email):
        return jsonify({"message" : "Please input a valid email"}), 400
    return jsonify({"message" : "Account created successfully"}), 201
    
    
    

@app.route('/api/v1/rides',  methods = ['POST'])
def create_ride():

     """
    Endpoint for creating a ride
    ---
    tags:
      - Ride
    parameters:
      - name: id
        in: path
        required: true
    responses:
      200:
        description: Fetch successfull
      404:
        description: Ride not created successfuly'
    """
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
    """
    Endpoint for getting rides
    ---
    tags:
      - Ride
    parameters:
      - name: id
        in: path
        required: true
    responses:
      200:
        description: Fetch successfull
      404:
        description: There are no rides to display'
    """
    trip = Ride()
    rides =  trip.get_all()

    return jsonify({'rides': rides})


@app.route('/api/v1/ride/<int:id>', methods = ['GET'])
def get_ride(id):
    """
    Endpoint for getting a ride
    ---
    tags:
      - Ride
    parameters:
      - name: id
        in: path
        required: true
    responses:
      200:
        description: Fetch successfull
      404:
        description: There is no ride to display'
    """
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
    """
    Endpoint for deleting a ride
    ---
    tags:
      - Ride
    parameters:
      - name: id
        in: path
        required: true
    responses:
      200:
        description: Fetch successfull
      404:
        description: There are no rides to display'
    """
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
    """
    Endpoint for getting a single request for a particular ride
    ---
    tags:
      - Request
    parameters:
      - name: ride_id
        in: path
        required: true
      - name: request_id
        in: path
        required: true
    responses:
      200:
        description: Fetch successfull
      404:
        description: There is no request for that ride'
    """
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



    