"""
Base Test case with setup and teadown methods that other
test classes inherit
"""
import unittest
import json
from app import create_app, db


class BaseTestCase(unittest.TestCase):
    """Base Test Case"""
    def setUp(self):
        """Set up test variables"""
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client()
        self.url = None
        self.data = None
        self.header = {'Content-Type': 'application/json'}

        with self.app.app_context():
            db.session.close()
            db.drop_all()
            db.create_all()

    def make_request(self, url, method='post', **kwargs):
        """This helper method makes a post request"""
        self.url = str(url)
        self.data = json.dumps(kwargs['data'])
        if method == 'put':
            return self.client.put(path=self.url, headers=self.header, data=self.data)
        elif method == 'delete':
            return self.client.delete(path=self.url, headers=self.header, data=self.data)
        return self.client.post(path=self.url, headers=self.header, data=self.data)

    def register_user(self, email="user@test.com", username="stephen",
                      password="test1234"):
        """This helper method helps register a test user"""
        user_data = {'email': email, 'username': username,
                     'password': password}
        return self.make_request('/api/v1/register', data=user_data)

    def login_user(self, email="user@test.com", password="test1234"):
        """This helper method helps log in a test user"""
        user_data = {'email': email, 'password': password}
        return self.make_request('/api/v1/login', data=user_data)

    def tearDown(self):
        """teardown all initialized variables"""
        with self.app.app_context():
            db.session.remove()
            db.drop_all()


if __name__ == "__main__":
    unittest.main()
