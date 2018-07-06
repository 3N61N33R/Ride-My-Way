import json
from tests.v2_tests.base_test import BaseTest

class TestAuth(BaseTest):
    def test_sign_up(self):
        response = self.app.post('/api/v2/auth/signup',data=json.dumps(self.user), headers={ 'content-type' : 'application/json'})
        self.assertEqual(response.status_code, 201)


    def test_login(self):
        self.app.post('/api/v2/auth/signup',data=json.dumps(self.user), headers={ 'content-type' : 'application/json'})
        res = self.app.post('/api/v2/auth/login',data=json.dumps(self.user), headers={ 'content-type' : 'application/json'})
        response = json.loads(res.data.decode())
        self.assertEqual(res.status_code, 200)
        self.assertTrue(response['access_token'])
