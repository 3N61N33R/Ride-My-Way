from flask import request, jsonify, make_response
import json 
from .models import User, Ride
from . import app


@app.route('/api/v1/users', methods = ['POST'])
def create_user():
    data = request.get_json()
    username = data['username']
    name = data['name']
    email = data['email']
    password = data['password']

    user = User(name=name, username=username, email=email, password=password)
    user.add()
    return jsonify({
                "message" : "Account created successfully"}), 201


@app.route('/api/v1/rides',  methods = ['POST'])
def create_ride():
    data = request.get_json()
    name = data['name']
    pickup = data['pickup']
    dropoff = data['dropoff']
    time = data['time']    

    ride = Ride( name = name, pickup = pickup , dropoff = dropoff,  time=time)
    ride.add()

    return (jsonify({
                "message" : "Ride created successfully"}), 201)


@app.route('/api/v1/rides')
def get_rides():
    trip = Ride()
    rides =  trip.get_all()

    return jsonify({'rides': rides})


@app.route('/api/v1/ride/<int:id>')
def get_ride(id):
    trip = Ride()
    ride =  trip.get_one(id)

    return jsonify({'ride': ride})

@app.route('/api/v1/ride/<int:id>',  methods = ['DELETE'])
def delete_ride(id):
    trip = Ride()
    ride =  trip.delete(id)

    return (jsonify({
                "message" : "Ride deleted successfully"}), 201)


    



    