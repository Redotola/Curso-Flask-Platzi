from flask import Flask, request, make_response, redirect, render_template, session, abort, url_for, flash
from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired
import unittest
import secrets
from flask_bootstrap import Bootstrap5

app = Flask(__name__) # the instance of Flask app is the name of the current file
bootstrap = Bootstrap5(app) # create the instance of Bootstrap Flask with the name of app

app.config['SECRET_KEY'] = secrets.token_hex(20)
app.config.update(ENV = 'development') # Set the environment to develop

# test list
todos = ["Wake Up", "Drink coffee", "Code", "Sleep"]

class LoginForm(FlaskForm): # We inherit the FlaskForm class to make a login form
        username = StringField('Username', validators = [DataRequired()]) # Create the values of login
        password = PasswordField("Password", validators = [DataRequired()])
        submit = SubmitField('Send')

# Errors
@app.errorhandler(404) # route that catch the error of not found the element required
def not_found(error):
    context = {
        'error' : error,
        'status' : 404,
        'text' : 'Element not found, error 404'
    }
    return render_template('error.html', **context) # return the render of template and error

@app.errorhandler(500) # error from the server or element
def internal_error_server(error): 
    context = {
        'error' : error,
        'status' : 500,
        'text' : 'Error de servidor, lo sentimos seguimos trabajando para solucionarlo...'
    }
    return render_template('error.html', **context) # render template

@app.route('/error')
def error_500():
    abort(500)

@app.cli.command()
def test():
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner().run(tests)
    

# index route
@app.route('/') # route of the function is working
def index():
    user_ip = request.remote_addr # obtain the ip of the user
    response = make_response(redirect('/hello')) # the index redirect to 'hello' route
    #response.set_cookie("user_ip", user_ip) # set the cookie in the browser with a name
    session['user_ip'] = user_ip
    return response

# homepage route
@app.route('/hello', methods = ['GET', 'POST'])
def hello():
    #user_ip = request.cookies.get('user_ip') # obtain the cookie from the browser
    login_form = LoginForm()
    user_ip = session.get('user_ip')
    username = session.get('username')
    
    context = {
        'user_ip' : user_ip,
        'todos' : todos,
        'login_form': login_form,
        'username' : username
    }
    
    #if the form is completed then the function redirect with the username in conectext
    if request.method == 'POST' or login_form.validate_on_submit(): 
        username = login_form.username.data
        session['username'] = username
        
        flash('Nombre de usuario registrado con exito', 'message')
        
        return redirect(url_for('index'))
    
    return render_template('hello.html', **context) # expand the dictionary 

# run app
if __name__ == "__main__": # if the file is explicit execute the server run
    app.run(port = 5500, host = "0.0.0.0", debug = True)
    