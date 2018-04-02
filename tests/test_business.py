"""Test case for the user"""
import json
import datetime
from flask_jwt_extended import create_access_token
from tests.test_base import BaseTestCase


class TestPostBusiness(BaseTestCase):
    """Test for post business endpoint"""
    def test_business_creation(self):
        """Test user registration works correcty"""
        result = self.register_business()
        self.assertEqual(result['message'], "Business created successfully")

    def test_create_empty_field(self):
        """Test business creation with an empty description"""
        result = self.register_business(name="KTDA", description=" ",
                          category="Farming", location="Narok")
        self.assertEqual(result['message'], ['Please enter your description'])
    
    def test_json_request(self):
        """Test business creation with absent content type header"""
        self.register_user()
        login_res = self.login_user()
        result = json.loads(login_res.data.decode())
        change_res = self.client.post(
            '/api/v1/business',
            headers={'Authorization': 'Bearer ' + result['access_token']},
            data={})
        result = json.loads(change_res.data.decode())
        self.assertEqual(result['message'], "Bad Request. Request should be JSON format")
        self.assertEqual(change_res.status_code, 405)

    def test_missing_user(self):
        """Test business for unregistered user"""
        business_data = {'name':'KTDA', 'description':'This is good', 'category':'Farming', 'location':'Narok'}
        access_token = create_access_token(identity=2, expires_delta=datetime.timedelta(hours=1))
        self.header['Authorization'] = 'Bearer ' + access_token
        res = self.make_request('/api/v1/business', data=business_data)
        result = json.loads(res.data.decode())
        self.assertEqual(result['message'], "Please login to continue")
