import unittest
from flask import current_app, url_for
from app import create_app

class TestComponent(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client(use_cookies=False)

    # Test to make index page show up
    def test_index(self):
        self.client.get(url_for('index'))
        self.assertTrue('Create New Question' in create)

    # Test create route for int
    def test_create_int(self):
        response = self.client.post(url_for('create'), data={
            'category': 'test question',
            'raw_question': 'int num = @A;---A, int, 5, 5'
        }, follow_redirects=True)
        self.assertTrue('int num = 6;' in response.data)
        print(response)

    def test_app_exists(self):
        self.assertFalse(current_app is None)

    def test_app_is_testing(self):
        self.assertTrue(current_app.config['TESTING'])

    def tearDown(self):
        self.app_context.pop()

if __name__ == "__main__":
    unittest.main()
