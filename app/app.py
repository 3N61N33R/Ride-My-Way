from flask import Flask, request, jsonify, make_response
import json 

app = Flask(__name__)

@app.route('/api/v1/users', methods = ['POST'])
def create_user():
    return make_response(jsonify({
                "message" : "Account created successfully"}), 201)


@app.route('/api/v1/rides',  methods = ['POST'])
def create_ride():
    return make_response(jsonify({
                "message" : "Ride created successfully"}), 201)

if __name__ == '__main__':
    app.run(debug=True)