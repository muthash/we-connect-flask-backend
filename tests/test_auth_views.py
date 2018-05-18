"""Test case for the user"""
import json
from tests.base_test_file import BaseTestCase


class TestRegisterUser(BaseTestCase):
    """Test for Register User endpoint"""
    def register(self, msg, code, key='message'):
        self.automate('/api/v1/register', key, data=self.reg_data,
                      msg=msg, code=code)

    def test_registration(self):
        """Test user registration works correcty"""
        result = json.loads(self.reg_res.data.decode())
        self.assertEqual(result['message'], "Account created successfully")
        self.assertEqual(self.reg_res.status_code, 201)

    def test_already_registered_user(self):
        """Test that a user cannot be registered twice"""
        self.register(msg="A User with that email already exists.", code=409)

    def test_register_missing_password(self):
        """Test user registration with missing password"""
        del self.reg_data['password']
        self.register(key='password-error', code=422,
                      msg="The password should not be missing")

    def test_register_empty_username(self):
        """Test user registration with empty username"""
        self.reg_data['username'] = "  "
        self.register(key='username-error', code=422,
                      msg="The username should not be empty")

    def test_register_safe_username(self):
        """Test user registration with reserved names"""
        self.reg_data['username'] = "login"
        self.register(code=400,
                      msg="The username you provided is not allowed, " +
                          "please try again but with a different name.")

    def test_invalid_password_pattern(self):
        """Test register with short password length"""
        self.reg_data['password'] = 'short'
        self.register(code=400,
                      msg='Password should contain at least eight characters' +
                          ' with at least one digit, one uppercase letter' +
                          ' and one lowercase letter')

    def test_invalid_username_pattern(self):
        """Test register with short password length"""
        self.reg_data['username'] = 'in'
        self.register(code=400,
                      msg="The Username should contain atleast four " +
                          "alpha-numeric characters. The optional " +
                          "special character allowed is _ (underscore).")

    def test_register_invalid_email(self):
        """Test user registration with an invalid email address"""
        self.reg_data['email'] = 'invalid'
        self.register(msg="The email address is not valid." +
                      " It must have exactly one @-sign.", code=400)

    def test_valid_json_request(self):
        """Test register request is json format"""
        del self.header['Content-Type']
        res = self.make_request('/api/v1/register', 'post', self.reg_data)
        result = json.loads(res.data.decode())
        self.assertEqual(result['message'],
                         "The Request should be JSON format")
        self.assertEqual(res.status_code, 422)


class TestLoginUser(BaseTestCase):
    """Test for Login User endpoint"""
    def login(self, msg, code, key='message'):
        self.automate('/api/v1/login', key, data=self.reg_data,
                      code=code, msg=msg)

    def test_user_login(self):
        """Test registered user can login"""
        self.login(code=200, msg='Login successfull')

    def test_login_empty_email(self):
        """Test user login with empty username"""
        self.reg_data['email'] = "  "
        self.login(key='email-error', code=422,
                   msg="The email should not be empty")

    def test_incorrect_password_login(self):
        """Test incorrect password cannot login"""
        self.reg_data['password'] = 'incorrect'
        self.login(code=401, msg='Invalid email or password')

    def test_unregistered_user_login(self):
        """Test unregistered user cannot login"""
        self.reg_data['email'] = 'unreg@test.com'
        self.login(code=401, msg='Invalid email or password')


class TestLogoutUser(BaseTestCase):
    """Test for Logout User endpoint"""
    def test_logout_user(self):
        """Test if logged in user can logout"""
        self.automate('/api/v1/logout', key='message', data=None, code=200,
                      msg='Successfully logged out')


class TestResetPassword(BaseTestCase):
    """Test reset password user endpoint"""
    def reset_password(self, code, msg, key='message'):
        self.automate('/api/v1/reset-password', key, data=self.reg_data,
                      code=code, msg=msg)

    def test_password_reset(self):
        """Test password reset works as expected"""
        self.reset_password(code=201,
                            msg='Password reset successfull.' +
                            ' Check your email for your new password')

    def test_reset_missing_email(self):
        """Test reset password with missing email"""
        del self.reg_data['email']
        self.reset_password(key='email-error', code=422,
                            msg="The email should not be missing")

    def test_reset_invalid_email(self):
        """Test reset password with invalid email"""
        self.reg_data['email'] = "email@"
        self.reset_password(code=400,
                            msg="There must be something after the @-sign.")

    def test_unregistered_user(self):
        """Test password change for unregistered user"""
        self.reg_data['email'] = "notuser@mail.com"
        self.reset_password(code=401,
                            msg='The email provided is not registered')


class TestChangetPassword(BaseTestCase):
    """Test change password user endpoint"""
    def change_password(self, msg, code, key='message'):
        self.automate('/api/v1/change-password', key, data=self.passwords,
                      code=code, method='put', msg=msg)

    def test_password_change(self):
        """Test password change works as expected"""
        self.change_password(code=201, msg='Password change successfull')

    def test_change_missing_password(self):
        """Test change password with missing password"""
        del self.passwords['old_password']
        self.change_password(key='old_password-error', code=422,
                             msg="The old_password should not be missing")

    def test_invalid_password_pattern(self):
        """Test change password with short password length"""
        self.passwords['new_password'] = 'short'
        self.change_password(code=400,
                             msg='Password should contain at least eight ' +
                                 'characters with at least one digit, one ' +
                                 'uppercase letter and one lowercase letter')

    def test_wrong_initial_password(self):
        """Test change password with incorrect old password"""
        self.passwords['old_password'] = 'wrongpass'
        self.change_password(code=401,
                             msg='Old password entered is not correct')


class TestDeleteAccount(BaseTestCase):
    """Test delete account user endpoint"""
    def delete_account(self, code, msg, key='message'):
        self.automate('/api/v1/delete-account', key, data=self.reg_data,
                      method='delete', code=code, msg=msg)

    def test_delete_account(self):
        """Test delete account works as expected"""
        self.delete_account(code=200, msg='Account deleted successfully')

    def test_delete_wrong_password(self):
        """Test delete account with incorrect password"""
        self.reg_data['password'] = 'wrong'
        self.delete_account(code=401,
                            msg='Old password entered is not correct')

    def test_delete_missing_password(self):
        """Test delete account with no password"""
        del self.reg_data['password']
        self.delete_account(code=422, key='password-error',
                            msg='The password should not be missing')

if __name__ == "__main__":
    unittest.main()
