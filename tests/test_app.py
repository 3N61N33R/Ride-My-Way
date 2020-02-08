
import os 
import json
import pytest

from app import app


@pytest.fixture
def test_client():
        app.config['TESTING'] = True
        client = app.test_client()
        
        ctx = app.app_context()
        ctx.push()
        yield client
        
        ctx.pop()



def test_create_user(test_client):
        user = {"name": "name","username":"gray", "email":"email@gmail.com","password":"bistro5"}
        response = test_client.post('/api/v1/users', data=json.dumps(user), headers={ 'content-type' : 'application/json'})
        assert response.status_code == 201

def test_create_ride(test_client):
        ride = {"name":"annie", "pickup":"juja","dropoff":"Kasarani","time":"6:00pm"}
        response = test_client.post('/api/v1/rides', data = json.dumps(ride), content_type = 'application/json')
        assert response.status_code == 201
    
def test_get_rides(test_client):

        """test to fetch all ride offers"""

        
        response = test_client.get('/api/v1/rides')
        assert response.status_code == 200

def test_get_ride(test_client):

        """test to get specific ride"""

        response = test_client.get('/api/v1/ride/1')
        assert response.status_code == 200

def test_update_ride(test_client):

        """test to update a ride offers"""
        
        ride = { "pickup":"juja","dropoff":"Kasarani"}
        response = test_client.put('/api/v1/ride/1', data = json.dumps(ride), headers={ 'content-type' : 'application/json'})
        assert response.status_code == 201


def test_delete_ride(test_client):
        # Create ride
        ride = {"name":"annie", "pickup":"juja","dropoff":"Kasarani","time":"6:00pm"}
        response = test_client.post('/api/v1/rides', data = json.dumps(ride), content_type = 'application/json')
        # delete ride
        response = test_client.delete('/api/v1/ride/1')
        assert response.status_code == 200

def test_create_request(test_client):
        ride = {"name":"annie", "pickup":"juja","dropoff":"Kasarani","time":"6:00pm"}
        response = test_client.post('/api/v1/rides', data = json.dumps(ride), content_type = 'application/json')
        
        request = {"name":"annie"}
        response = test_client.post('/api/v1/ride/5/request', data = json.dumps(request), headers={ 'content-type' : 'application/json'})
        assert response.status_code == 201


def test_get_requests(test_client):

        """test to fetch all ride requests"""
        
        response = test_client.get('/api/v1/ride/5/requests')
        assert response.status_code == 200

def test_get_request(test_client):

        """test to fetch specific ride requests"""
        
        response = test_client.get('/api/v1/ride/5/request/1')
        assert response.status_code == 200


def test_delete_request(test_client):
        response = test_client.delete('/api/v1/ride/5/request/1')
        assert response.status_code == 200


    