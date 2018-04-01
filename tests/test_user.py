"""Test case for the user"""
import json
from unittest.mock import patch, Mock
from smtplib import SMTPException
from tests.test_base import BaseTestCase


# class TestRegisterUser(BaseTestCase):
#     """Test for Register User endpoint"""
#     def invalid_user_data(self, user_data):
#         """Helper for registration with invalid user data"""
#         res = self.make_request('/api/v1/register', data=user_data)
#         self.assertTrue(res.content_type == 'application/json')
#         self.assertEqual(res.status_code, 400)
#         result = json.loads(res.data.decode())
#         return result

#     def test_registration(self):
#         """Test user registration works correcty"""
#         res = self.register_user()
#         self.assertTrue(res.content_type == 'application/json')
#         result = json.loads(res.data.decode())
#         self.assertEqual(result['message'], "Account created successfully")
#         self.assertEqual(res.status_code, 201)

#     def test_already_registered_user(self):
#         """Test that a user cannot be registered twice"""
#         self.register_user()
#         second_res = self.register_user()
#         self.assertTrue(second_res.content_type == 'application/json')
#         result = json.loads(second_res.data.decode())
#         self.assertEqual(result['message'], "User already exists")
#         self.assertEqual(second_res.status_code, 409)

#     def test_register_invalid_email(self):
#         """Test user registration with an invalid email address"""
#         user_data = {'email': "test", 'username': "ian", 'password': "test"}
#         result = self.invalid_user_data(user_data)
#         self.assertEqual(result['message'], 'Please enter a valid email address')

#     def test_register_empty_username(self):
#         """Test user registration with an empty username"""
#         user_data = {'email': "test@test.com", 'username': "  ", 'password': "test"}
#         result = self.invalid_user_data(user_data)
#         self.assertEqual(result['message'], ['Please enter your username'])

#     def test_register_missing_field(self):
#         """Test use registration with missing password field"""
#         user_data = {'email': "test@test.com", 'username': "ian"}
#         result = self.invalid_user_data(user_data)
#         self.assertEqual(result['message'], ['Please enter your password'])

#     def test_json_request(self):
#         """Test register request for valid json"""
#         user_data = {'email': "test@test.com", 'username': "ian", 'password': "test"}
#         res = self.client.post('/api/v1/register', data=user_data)
#         self.assertEqual(res.status_code, 405)
#         result = json.loads(res.data.decode())
#         self.assertEqual(result['message'], 'Bad Request. Request should be JSON format')


# class TestLoginUser(BaseTestCase):
#     """Test for Login User endpoint"""
#     def test_user_login(self):
#         """Test registered user can login"""
#         self.register_user()
#         res = self.login_user()
#         self.assertTrue(res.content_type == 'application/json')
#         result = json.loads(res.data.decode())
#         self.assertEqual(result['message'], "Login successfull")
#         self.assertEqual(res.status_code, 200)
#         self.assertTrue(result['access_token'])

#     def test_unregistered_user_login(self):
#         """Test unregistered user cannot login"""
#         login_res = self.login_user('muthama@gmail.com', 'mypassword')
#         result = json.loads(login_res.data.decode())
#         self.assertEqual(result['message'], "Invalid email or password")
#         self.assertEqual(login_res.status_code, 401)

#     def test_json_request(self):
#         """Test login request for valid json"""
#         user_data = {'email': "test@test.com", 'password': "test"}
#         res = self.client.post('/api/v1/login', data=user_data)
#         self.assertEqual(res.status_code, 405)
#         result = json.loads(res.data.decode())
#         self.assertEqual(result['message'], 'Bad Request. Request should be JSON format')

#     def test_login_missing_field(self):
#         """Test use registration with missing password field"""
#         user_data = {'email': "test@test.com"}
#         res = self.make_request('/api/v1/login', data=user_data)
#         self.assertEqual(res.status_code, 400)
#         result = json.loads(res.data.decode())
#         self.assertEqual(result['message'], ['Please enter your password'])

# class TestLogoutUser(BaseTestCase):
#     """Test for Logout User endpoint"""
#     def test_logout_user(self):
#         """Test if logged in user can logout"""
#         self.get_login_token()
#         logout_res = self.client.post('/api/v1/logout', headers=self.header)
#         result = json.loads(logout_res.data.decode())
#         self.assertEqual(result['message'], "Successfully logged out")
#         self.assertEqual(logout_res.status_code, 200)

#     def test_already_logout_user(self):
#         """Test logout for aleady logged out user"""
#         self.get_login_token()
#         self.client.post('/api/v1/logout', headers=self.header)
#         logout_res = self.client.post('/api/v1/logout', headers=self.header)
#         result = json.loads(logout_res.data.decode())
#         self.assertEqual(result['msg'], "Token has been revoked")
#         self.assertEqual(logout_res.status_code, 401)


# class TestResetPassword(BaseTestCase):
#     """Test reset password user endpoint"""
#     def test_password_reset(self):
#         """Test password reset"""
#         self.register_user()
#         reset_res = self.make_request('/api/v1/reset-password', data=dict(email='user@test.com'))
#         result = json.loads(reset_res.data.decode())
#         self.assertEqual(result['message'], "An email has been sent with your new password")
#         self.assertEqual(reset_res.status_code, 201)

#     def test_json_request(self):
#         """Test reset password request for valid json"""
#         res = self.client.post('/api/v1/reset-password', data=dict(email='user@test.com'))
#         self.assertEqual(res.status_code, 405)
#         result = json.loads(res.data.decode())
#         self.assertEqual(result['message'], 'Bad Request. Request should be JSON format')

#     def test_reset_non_existing_email(self):
#         """Test reset password with a non existing account"""
#         reset_res = self.make_request('/api/v1/reset-password', data=dict(email='none@test.com'))
#         result = json.loads(reset_res.data.decode())
#         self.assertEqual(result['message'], "Please enter a valid email address")
#         self.assertEqual(reset_res.status_code, 401)

#     def test_reset_invalid_email(self):
#         """Test reset password with an invalid email address"""
#         reset_res = self.make_request('/api/v1/reset-password', data=dict(email='usertest'))
#         result = json.loads(reset_res.data.decode())
#         self.assertEqual(result['message'], "Please enter a valid email address")
#         self.assertEqual(reset_res.status_code, 400)


class TestChangetPassword(BaseTestCase):
    """Test change password user endpoint"""
    def test_password_change(self):
        """Test password change"""
        passwords = {'old_password': "test1234", 'new_password': "newtestpass"}
        self.get_login_token()
        change_res = self.make_request('/api/v1/change-password', data=passwords, method='put')
        result = json.loads(change_res.data.decode())
        self.assertEqual(result['message'], "Password changed successfully")
        self.assertEqual(change_res.status_code, 200)

    def test_incorrect_initial_password(self):
        """Test password with incorrect old password input"""
        passwords = {'old_password': "test123", 'new_password': "newtestpass"}
        self.get_login_token()
        change_res = self.make_request('/api/v1/change-password', data=passwords, method='put')
        result = json.loads(change_res.data.decode())
        self.assertEqual(result['message'], "Invalid password")
        self.assertEqual(change_res.status_code, 401)

    def test_json_request(self):
        """Test change password request for valid json"""
        passwords = {'old_password': "test123", 'new_password': "newtestpass"}
        self.register_user()
        login_res = self.login_user()
        result = json.loads(login_res.data.decode())
        self.header['Authorization'] = 'Bearer ' + result['access_token']
        change_res = self.client.put(
            '/api/v1/change-password',
            headers={'Authorization': 'Bearer ' + result['access_token']},
            data=passwords)
        result = json.loads(change_res.data.decode())
        self.assertEqual(result['message'], "Bad Request. Request should be JSON format")
        self.assertEqual(change_res.status_code, 405)

    def test_invalid_initial_password(self):
        """Test password with incorrect old password input"""
        passwords = {'old_password': "test123", 'new_password': "  "}
        self.get_login_token()
        change_res = self.make_request('/api/v1/change-password', data=passwords, method='put')
        result = json.loads(change_res.data.decode())
        self.assertEqual(result['message'], ['Please enter your new_password'])
        self.assertEqual(change_res.status_code, 400)

#     def test_delete_account(self):
#         """Test deleting account"""
#         self.register_user()
#         login_res = self.login_user()
#         result = json.loads(login_res.data.decode())
#         self.header['Authorization'] = 'Bearer ' + result['access_token']
#         res = self.make_request('/api/v1/delete-account', data=dict(password='test1234'), method='delete')
#         result = json.loads(res.data.decode())
#         self.assertEqual(result['message'], "Account deleted successfully")
#         self.assertEqual(res.status_code, 200)
