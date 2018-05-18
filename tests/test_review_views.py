"""Test case for review manipulation view"""
import json
from tests.base_test_file import BaseTestCase


class TestPostReview(BaseTestCase):
    """Test for post review endpoint"""
    def create_review(self, msg, code, key='message'):
        self.automate('/api/v1/businesses/1/reviews', key,
                      data=self.review_data, code=code, msg=msg)

    def test_review_creation(self):
        """Test create review works correcty"""
        with self.app.app_context():
            self.reg_data['email'] = 'anotheruser@test.com'
            self.make_request('/api/v1/register', 'post', data=self.reg_data)
            self.get_login_token(self.reg_data)
            self.create_review(code=201,
                               msg='Review for business with id 1 created')

    def test_review_own_business(self):
        """Test create review by business owner"""
        self.create_review(code=403,
                           msg='The operation is forbidden for own business')

    def test_empty_review_creation(self):
        """Test create review with missing data"""
        with self.app.app_context():
            self.review_data = {}
            self.reg_data['email'] = 'anotheruser@test.com'
            self.make_request('/api/v1/register', 'post', data=self.reg_data)
            self.get_login_token(self.reg_data)
            self.create_review(code=422, key="rating-error",
                               msg='The rating should not be missing')

    def test_get_reviews(self):
        """Test get all reviews for a business"""
        with self.app.app_context():
            self.reg_data['email'] = 'anotheruser@test.com'
            self.make_request('/api/v1/register', 'post', data=self.reg_data)
            self.get_login_token(self.reg_data)
            self.create_review(code=201,
                               msg='Review for business with id 1 created')
            res = self.client.get('/api/v1/businesses/1/reviews')
            result = json.loads(res.data.decode())
            self.assertTrue(result['reviews'])
