import unittest
from flask import current_app
from app import create_app

class SampleTest(unittest.TestCase):
  def setUp(self):
    self.app = create_app('testing')
    self.app_context = self.app.app_context()
    self.app_context.push()

  def tearDown(self):
    self.app_context.pop()

  # Test to make sure question can be created
  def test_value(self):
    response - self.client.post(url_for('create'), data={
      'category': 'test',
      'question': 'this is a test question'
    }, follow_redirects=True)
    self.assertTrue()

  def test_app_exists(self):
    self.assertFalse(current_app is None)

  def test_app_is_testing(self):
    self.assertTrue(current_app.config['TESTING'])
