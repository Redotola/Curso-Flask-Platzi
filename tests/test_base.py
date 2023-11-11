from flask_testing import TestCase
from flask import current_app, url_for
from app import app


class MainTest(TestCase):

    def create_app(self):
        app.config['TESTING'] = True # Create the environment of testing
        app.config['WTF_CSRF_ENABLED'] = False # if it send a form is required a token encrypted
        
        return app
    
    def test_app_exists(self):
        self.assertIsNotNone(current_app) # check if the app exist
    
    def test_app_in_test_mode(self):
        #check if the app is running in TESTING environment
        self.assertTrue(current_app.config['TESTING']) 
    
    def test_index_redirects(self):
        response = self.client.get(url_for('index')) # obtain the response of test the index redirect
        self.assertRedirects(response, url_for('hello')) 
        '''
        if this cause a problem in the 3 test:
        - Go to definition of "assertRedirects"
        - In line 304 "if parts.netloc:" try "if parts.path:" instead
        '''
    def test_hello_get(self):
        response = self.client.get(url_for('hello')) # check if the response is 200
        self.assert200(response)
        
    def test_hello_post(self):
        fake_form = {
            'username': 'fake', # create a fake user from a form
            'password': 'fake-password'
        }
        response = self.client.post(url_for('hello'), data = fake_form)
        
        self.assertRedirects(response, url_for('index'))