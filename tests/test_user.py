"""Test case for the user"""
import json
from tests.test_base import BaseTestCase


class AuthTestCase(BaseTestCase):
    """Test case for the user"""
    def test_registration(self):
        """Test user registration works correcty."""
        res = self.register_user()
        result = json.loads(res.data.decode())
        self.assertEqual(result['message'], "You registered successfully")
        self.assertEqual(res.status_code, 201)
