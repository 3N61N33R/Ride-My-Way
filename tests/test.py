from app import app
import unittest
import json

class AppTestCase(unittest.TestCase):

    def setUp(self):
        app.testing = True
        self.app = app.test_client()

    def test_create_user(self):
        user = {"username":"gray", "email":"email@gmail.com","password":"bistro5"}
        response = self.app.post('/api/v1/users', data=json.dumps(user))
        self.assertEqual(response.status_code, 201)

    def test_create_ride(self):
        ride = {"name":"annie", "pickup":"juja","drop_off":"Kasarani"}
        response = self.app.post('/api/v1/rides', data = json.dumps(ride), content_type = 'application/json')
        self.assertEqual(response.status_code, 201)
    
    
    def test_get_ride(self):

        """test to fetch all ride offers"""

        
        response = self.app.get('/api/v1/rides')
        self.assertEqual(response.status_code, 200)

    def test_get_one_ride(self):

        """test to get specific ride"""

        response = self.app.get('/api/v1/rides/10')
        self.assertEqual(response.status_code, 200)

    def test_update_ride(self):

        """test to update a ride offers"""
        
        ride = {"name":"annie", "pickup":"juja","drop_off":"Kasarani"}
        response = self.app.put('/api/v1/rides/6', data = json.dumps(ride), content_type = 'application/json')
        self.assertEqual(response.status_code, 200)

    def test_delete_ride(self):
        response = self.app.delete('/api/v1/rides/1')
        self.assertEqual(response.status_code, 200)


    def test_get_request(self):

        """test to fetch all ride requests"""
        
        response = self.app.get('/api/v1/rides/1/requests')
        self.assertEqual(response.status_code, 200)

    def test_get_one_request(self):

        """test to fetch specific ride requests"""
        
        response = self.app.get('/api/v1/rides/2/requests/1')
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()

    