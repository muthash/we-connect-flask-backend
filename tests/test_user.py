"""Test case for the user"""
import json
from tests.test_base import BaseTestCase


class AuthTestCase(BaseTestCase):
    """Test case for the user"""
    # def test_registration(self):
    #     """Test user registration works correcty"""
    #     res = self.register_user()
    #     self.assertTrue(res.content_type == 'application/json')
    #     result = json.loads(res.data.decode())
    #     self.assertEqual(result['message'], "Account created successfully")
    #     self.assertEqual(res.status_code, 201)

    # def test_already_registered_user(self):
    #     """Test that a user cannot be registered twice"""
    #     self.register_user()
    #     second_res = self.register_user()
    #     self.assertTrue(second_res.content_type == 'application/json')
    #     result = json.loads(second_res.data.decode())
    #     self.assertEqual(result['message'], "User already exists")
    #     self.assertEqual(second_res.status_code, 409)

    # def test_user_login(self):
    #     """Test registered user can login"""
    #     self.register_user()
    #     res = self.login_user()
    #     self.assertTrue(res.content_type == 'application/json')
    #     result = json.loads(res.data.decode())
    #     self.assertEqual(result['message'], "Login successfull")
    #     self.assertEqual(res.status_code, 200)
    #     self.assertTrue(result['access_token'])

    # def test_unregistered_user_login(self):
    #     """Test unregistered user cannot login"""
    #     login_res = self.login_user('muthama@gmail.com', 'mypassword')
    #     result = json.loads(login_res.data.decode())
    #     self.assertEqual(result['message'], "Invalid email or password, " +
    #                      "Please try again")
    #     self.assertEqual(login_res.status_code, 401)

    # def test_logout_user(self):
    #     """Test if logged in user can logout"""
    #     self.register_user()
    #     res = self.login_user()
    #     access_token = json.loads(res.data.decode())['access_token']
    #     logout_res = self.client.post(
    #         '/api/v1/logout',
    #         headers={'Content-Type': 'application/json',
    #                  'Authorization': 'Bearer ' + access_token})
    #     result = json.loads(logout_res.data.decode())
    #     self.assertEqual(result['message'], "Successfully logged out")
    #     self.assertEqual(logout_res.status_code, 200)

    # def test_password_reset(self):
    #     """Test password reset"""
    #     self.register_user()
    #     reset_res = self.make_request('/api/v1/reset-password', data=dict(email='user@test.com'))
    #     result = json.loads(reset_res.data.decode())
    #     self.assertEqual(result['message'], "An email has been sent with your new password")
    #     self.assertEqual(reset_res.status_code, 201)

    # def test_password_change(self):
    #     """Test setting of new password"""
    #     self.register_user()
    #     reset_res = self.make_request('/api/v1/reset-password', data=dict(email='user@test.com'))
    #     result = json.loads(reset_res.data.decode())
    #     passwords = {'old_password': result['password'], 'new_password': 'newtestpass'}
    #     login_res = self.login_user('user@test.com', result['password'])
    #     result_ = json.loads(login_res.data.decode())
    #     self.header['Authorization'] = 'Bearer ' + result_['access_token']
    #     change_res = self.make_request('/api/v1/change-password', data=passwords, method='put')
    #     result_c = json.loads(change_res.data.decode())
    #     self.assertEqual(result_c['message'], "Password changed successfully")
    #     self.assertEqual(change_res.status_code, 200)

    def test_delete_account(self):
        """Test deleting account"""
        self.register_user()
        login_res = self.login_user()
        result = json.loads(login_res.data.decode())
        access_token = json.loads(login_res.data.decode())['access_token']
        self.header['Authorization'] = 'Bearer ' + result['access_token']
        res = self.make_request('/api/v1/delete-account', data=dict(password='test1234'), method='delete')
        result = json.loads(res.data.decode())
        self.assertEqual(result['message'], "Account deleted successfully")
        self.assertEqual(res.status_code, 200)
