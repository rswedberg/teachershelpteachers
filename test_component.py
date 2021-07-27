import unittest
from flask import current_app, url_for
from app import app, create_app

class TestComponent(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app_context = self.app.test_request_context()
        self.app_context.push()
        self.client = self.app.test_client(use_cookies=True)

    # Test to verify redirect to login page
    def test_index(self):
        # Initiate app to run
        tester = app.test_client(self)
        # Run get request for / route
        response = tester.get('/')
        # Look for string in html file
        self.assertIn(b'Login with Google', response.data)

    # Test to verify instructions are given for the create page
    def test_create_view(self):
        # Initiate app to run
        tester = app.test_client(self)
        # Run get request for /create route
        response = tester.get('/create')
        # Look for string in html file
        self.assertIn(b'Instructions:', response.data)

    # Test create route for int
    def test_create_int(self):
        # Initiate app to run
        tester = app.test_client(self)
        # Run post request for /create route passing values for all request.form
        response = tester.post('/create', data={
            'category': 'test question',
            'code': 'int num = @A;---A, int, 5, 5',
            'action': 'view'
        }, follow_redirects=True)
        # Look for string in html to verify previewed code looks as expected
        self.assertIn(b'int num = 5;', response.data)

    # Test create route for float
    def test_create_float(self):
        # Initiate app to run
        tester = app.test_client(self)
        # Run post request for /create route passing values for all request.form
        response = tester.post('/create', data={
            'category': 'test question',
            'code': 'double num = @A;---A, float, 1, 3.3, 3.3',
            'action': 'view'
        }, follow_redirects=True)
        # Look for string in html to verify previewed code looks as expected
        self.assertIn(b'double num = 3.3;', response.data)


    # Test create route for string
    def test_create_string(self):
        # Initiate app to run
        tester = app.test_client(self)
        # Run post request for /create route passing values for all request.form
        response = tester.post('/create', data={
            'category': 'test question',
            'code': 'String s = @A;---A, str, hi',
            'action': 'view'
        }, follow_redirects=True)
        # Look for string in html to verify previewed code looks as expected
        self.assertIn(b'String s = hi;', response.data)

    # Test create route for storing a question
    """     def test_create_store(self):
        # Initiate app to run
        tester = app.test_client(self)
        # Run post request for /create route passing values for all request.form
        response = tester.post('/create', data={
            'category': 'test question',
            'user': 'author.email',
            'code': 'String s = @A;---A, str, hi',
            'action': 'store'
        }, follow_redirects=True)
        # Look for string in html to verify previewed code looks as expected
        self.assertIn(b'saved', response.data) """


    # Test to verify search is given for the retrieve page
    def test_retrieve_view(self):
        # Initiate app to run
        tester = app.test_client(self)
        # Run get request for /create route
        response = tester.get('/retrieve')
        # Look for string in html file
        self.assertIn(b'search', response.data)
    

    # Test retrieve route for category only
    def test_create_retrieve_cat(self):
        # Initiate app to run
        tester = app.test_client(self)
        # Run post request for /create route passing values for all request.form
        response = tester.post('/retrieve', data={
            'search_method': 'category',
            'categories': 'Milestone Test'
        }, follow_redirects=True)
        # Look for string in html to verify previewed code looks as expected
        self.assertIn(b'^^^^', response.data)

    # Test retrieve route for author only
    def test_create_retrieve_author(self):
        # Initiate app to run
        tester = app.test_client(self)
        # Run post request for /create route passing values for all request.form
        response = tester.post('/retrieve', data={
            'search_method': 'author',
            'author': 'mzietlow@unomaha.edu'
        }, follow_redirects=True)
        # Look for string in html to verify previewed code looks as expected
        self.assertIn(b'^^^^', response.data)

    # Test retrieve route for both category and author
    def test_create_retrieve_both(self):
        # Initiate app to run
        tester = app.test_client(self)
        # Run post request for /create route passing values for all request.form
        response = tester.post('/retrieve', data={
            'search_method': 'both',
            'categories': 'Test Question',
            'author': 'mzietlow@unomaha.edu'
        }, follow_redirects=True)
        # Look for string in html to verify previewed code looks as expected
        self.assertIn(b'^^^^', response.data)

    # ADD TEST FOR MULTIPLE QUESTIONS

    # Test that app exists 
    def test_app_exists(self):
        self.assertFalse(current_app is None)

    def tearDown(self):
        self.app_context.pop()

if __name__ == "__main__":
    unittest.main()
