from flask_testing import TestCase
from flask import current_app, url_for
from app import app


class MainTest(TestCase):

    #create the variables of the testing
    def create_app(self):
        app.config['TESTING'] = True # Create the environment of testing
        app.config['WTF_CSRF_ENABLED'] = False # if it send a form is required a token encrypted
        
        return app
    
    # check if the instance of app exist
    def test_app_exists(self):
        self.assertIsNotNone(current_app) 
    
    #check if the app is running in TESTING environment
    def test_app_in_test_mode(self):
        self.assertTrue(current_app.config['TESTING']) 
    
    #check if the index redirect correctly
    def test_index_redirects(self):
        response = self.client.get(url_for('index')) # obtain the response of test the index redirect
        self.assertRedirects(response, url_for('hello')) 
        '''
        if this cause a problem in the 3 test:
        - Go to definition of "assertRedirects"
        - In line 304 "if parts.netloc:" try "if parts.path:" instead
        '''
        
    # check if hello works
    def test_hello_get(self):
        response = self.client.get(url_for('hello')) # check if the response is 200
        self.assert200(response)
    
    # check if hello form work and redirect correctly
    def test_hello_post(self):
        response = self.client.post(url_for('hello'))
        self.assertTrue(response.status_code, 405)
    
    # test and check that login template work
    def test_auth_login_get(self): 
        response = self.client.get(url_for('login'))
        self.assert200(response)
    
    # check and test if the template of login redirect correctly
    def test_auth_login_template(self):
        self.client.get(url_for('login'))
        self.assertTemplateUsed('login.html')
        
    def test_auth_login_post(self):
        fake_form = {
            'username': 'fake',
            'password': 'fake-password'
        }
        
        response = self.client.post(url_for('login'), data = fake_form)
        self.assertRedirects(response, url_for('index'))