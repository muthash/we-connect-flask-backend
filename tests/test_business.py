"""Test case for the user"""
import json
from tests.test_base import BaseTestCase


class TestPostBusiness(BaseTestCase):
    """Test for post business endpoint"""
    def test_business_creation(self):
        """Test user registration works correcty"""
        result = self.register_business()
        self.assertEqual(result['message'], "Account created successfully")
