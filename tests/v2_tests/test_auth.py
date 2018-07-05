# import json
# from tests.v2_tests.base_test import BaseTest

# class TestAuth(BaseTest):
#     def test_sign_up(self):
#         user = ()
#         response = BaseTest.create_app().post('/api/v2/auth/signup',data=json.dumps(user), headers={ 'content-type' : 'application/json'})
#         self.assertEqual(response.status_code, 201)


#     def test_login(self):
#         response = self.create_app().post('/api/v2/auth/login',data=json.dumps(user), headers={ 'content-type' : 'application/json'})
#         self.assertEqual(response.status_code, 201)
