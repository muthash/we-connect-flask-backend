"""
Base Test case with setup and methods that other
test classes inherit
"""
import unittest
import json
import datetime
from flask_jwt_extended import create_access_token
from app import create_app, db


class BaseTestCase(unittest.TestCase):
    """Base Test Case"""
    def setUp(self):
        """Set up test variables"""
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client()
        with self.app.app_context():
            db.drop_all()
            db.create_all()
            self.expires = datetime.timedelta(minutes=2)
            self.token = create_access_token(identity='notuser@mail.com',
                                             expires_delta=self.expires)

        self.header = {'Content-Type': 'application/json'}

        self.reg_data = {'email': 'user@test.com', 'username': 'stephen',
                         'password': 'Tests12!@'}
        self.reg_res = self.make_request('/api/v1/register', 'post',
                                         data=self.reg_data)
        self.get_login_token(self.reg_data)
        self.passwords = {'old_password': 'Tests12!@',
                          'new_password': 'Test123#$'}
        # self.get_login_token(self.reg_data)
        # self.business_data = {'name': 'Andela', 'category': 'IT',
        #                       'location': 'Nairobi'}
        # self.biz_res = self.make_request('/api/v1/businesses', 'post',
        #                                  data=self.business_data)
        # self.password = {'password': 'Test1234'}

        # self.review_data = {'review': 'Andela is the BEST. TIA'}
        # with self.app.app_context():
        #     self.expires = datetime.timedelta(minutes=2)
        #     self.token = create_access_token(identity='notuser@mail.com',
        #                                      expires_delta=self.expires)

        

    def make_request(self, url, method, data):
        """Make a request to the given url with the given method"""
        data = json.dumps(data)
        if method == 'put':
            return self.client.put(path=url,
                                   headers=self.header, data=data)
        elif method == 'delete':
            return self.client.delete(path=url,
                                      headers=self.header, data=data)
        return self.client.post(path=url, headers=self.header, data=data)

    def automate(self, url, key, method='post', **kwargs):
        """Make the test to a given url"""
        data = kwargs['data']
        message = kwargs['msg']
        code = kwargs['code']
        res = self.make_request(url, method, data)
        result = json.loads(res.data.decode())
        self.assertEqual(result[key], message)
        self.assertEqual(res.status_code, code)

    def get_login_token(self, data):
        """Get the access token and add it to the header"""
        login_res = self.make_request('/api/v1/login', 'post', data=data)
        result = json.loads(login_res.data.decode())
        self.header['Authorization'] = 'Bearer ' + result['access_token']
        return result

    def tearDown(self):
        """teardown all initialized variables"""
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

if __name__ == "__main__":
    unittest.main()