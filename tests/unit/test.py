from app import app 

import json



def test_create_user(test_client):
        user = {"username":"gray", "email":"email@gmail.com","password":"bistro5"}
        response = test_client.post('/api/v1/users', data=json.dumps(user))
        test_client.assertEqual(response.status_code, 201)

def test_create_ride(test_client):
        ride = {"name":"annie", "pickup":"juja","drop_off":"Kasarani"}
        response = test_client.post('/api/v1/rides', data = json.dumps(ride), content_type = 'application/json')
        test_client.assertEqual(response.status_code, 201)
    
    
def test_get_ride(test_client):

        """test to fetch all ride offers"""

        
        response = test_client.get('/api/v1/rides')
        test_client.assertEqual(response.status_code, 200)

def test_get_one_ride(test_client):

        """test to get specific ride"""

        response = test_client.get('/api/v1/rides/10')
        test_client.assertEqual(response.status_code, 200)

def test_update_ride(test_client):

        """test to update a ride offers"""
        
        ride = {"name":"annie", "pickup":"juja","drop_off":"Kasarani"}
        response = test_client.put('/api/v1/rides/6', data = json.dumps(ride), content_type = 'application/json')
        test_client.assertEqual(response.status_code, 200)

def test_delete_ride(test_client):
        response = test_client.delete('/api/v1/rides/1')
        test_client.assertEqual(response.status_code, 200)

def test_get_request(test_client):

        """test to fetch all ride requests"""
        
        response = test_client.get('/api/v1/rides/1/requests')
        test_client.assertEqual(response.status_code, 200)

def test_get_one_request(test_client):

        """test to fetch specific ride requests"""
        
        response = test_client.get('/api/v1/rides/2/requests/1')
        test_client.assertEqual(response.status_code, 200)


    