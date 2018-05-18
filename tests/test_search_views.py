"""Test case for search manipulation view"""
import json
from tests.base_test_file import BaseTestCase


class TestSearchBusiness(BaseTestCase):
    """Test for search business endpoint"""
    def search_business(self, url):
        res = self.client.get(path=url)
        return json.loads(res.data.decode())

    def test_search_businesses(self):
        """Test search available registered businesses"""
        result = self.search_business('/api/v1/search?q=and')
        self.assertTrue(result)

    def test_missing_q(self):
        """Test search missing q"""
        result = self.search_business('/api/v1/search?')
        self.assertEqual(result['search_parameter-error'],
                         "The search_parameter should not be empty")

    def test_not_matching_criteria(self):
        """Test search with not available criteria"""
        result = self.search_business('/api/v1/search?q=saf')
        self.assertEqual(result['message'],
                         "The search for saf did not match any business")

    def test_search_with_filter(self):
        """Test search with filter criteria"""
        result = self.search_business('/api/v1/search?q=and&cat=IT')
        self.assertTrue(result['businesses'])
