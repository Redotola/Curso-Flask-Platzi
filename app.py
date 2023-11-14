from flask import Flask, request, make_response, redirect, render_template, session, abort, url_for, flash
from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired
import unittest
import secrets
from flask_bootstrap import Bootstrap5
from services.fire_store_service import get_todos, get_user_by_id, user_put, put_todo, delete_todo, update_todo
from flask_login import LoginManager, login_required, login_manager, login_user, current_user, logout_user
from models.user import UserModel, UserData
from werkzeug.security import generate_password_hash, check_password_hash

login_manager = LoginManager()
login_manager.login_view = 'login'

app = Flask(__name__) # the instance of Flask app is the name of the current file
bootstrap = Bootstrap5(app) # create the instance of Bootstrap Flask with the name of app
login_manager.init_app(app)

app.config['SECRET_KEY'] = secrets.token_hex(20)
app.config.update(ENV = 'development') # Set the environment to develop


#Formulary

class LoginForm(FlaskForm): # We inherit the FlaskForm class to make a login form
        username = StringField('Username', validators = [DataRequired()]) # Create the values of login
        password = PasswordField("Password", validators = [DataRequired()])
        submit = SubmitField('Send')
        
class TodoForm(FlaskForm):
    description = StringField('Description', validators=[DataRequired()])
    submit = SubmitField('Create')
    
class DeleteForm(FlaskForm):
    submit = SubmitField('DELETE')
    
class UpdateForm(FlaskForm):
    submit = SubmitField('UPDATE')

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
        'text' : 'We are sorry this is a error server, we are working to fix it...'
    }
    return render_template('error.html', **context) # render template

@app.route('/error') #run the error 500 route 
def error_500():
    abort(500)

@app.cli.command() # cli command to run the environment of the test
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
@login_required
def hello():
    if current_user.is_authenticated:
        user_ip = session.get('user_ip')
        username = current_user.id
        todo_form = TodoForm()
        delete_todo_form = DeleteForm()
        update_todo_form = UpdateForm()

        # The context dictionary that allow us to save the user data
        context = {
            'user_ip' : user_ip,
            'todos' : get_todos(user_id = username),
            'username' : username,
            'todo_form': todo_form,
            'delete_todo_form': delete_todo_form,
            'update_todo_form': update_todo_form,
        }

        # if the data form 
        if todo_form.validate_on_submit(): 
            put_todo(user_id=username, description=todo_form.description.data)
            flash('Your to-do was succesfull created')
            return redirect(url_for('hello'))

        return render_template('hello.html', **context) # expand the dictionary 
    else:
        flash('You need to login first')
        return redirect(url_for('login'))
    
# Method to delete a todo from the list of the user
@app.route('/todos/delete/<todo_id>', methods=['GET', 'POST'])
def delete(todo_id):
    delete_todo_form = DeleteForm()
    if delete_todo_form.validate_on_submit():
        user_id = current_user.id
        print(todo_id*3)
        delete_todo(user_id=user_id, todo_id=todo_id)
    return redirect(url_for('hello'))

@app.route('/todos/update/<todo_id>/<int:done>', methods=['GET' ,'POST'])
def update(todo_id, done):
    user_id = current_user.id
    print('DONE', done)
    update_todo(user_id=user_id, todo_id=todo_id, done=done)
    return redirect(url_for('hello'))
    
    
@app.route('/login', methods=['GET', 'POST']) 
def login():
    login_form = LoginForm()
    context = {
        'login_form': login_form
    }
    
    #if the form was submited correctly
    if login_form.validate_on_submit(): 
        username = login_form.username.data
        password = login_form.password.data
        
        user_doc = get_user_by_id(username) # get the id by the username
        
        if user_doc.to_dict() is not None: # if the collection is not null
            
            if check_password_hash(user_doc.to_dict()['password'], password): # if password == password from DB
                user_data = UserData(username, password) # Create user with data in object
                user = UserModel(user_data)
                login_user(user) # Login with the user
                flash('Welcome again user {}'.format(user_data.username))
                redirect(url_for('hello'))
            else:
                flash("The username or the password is incorrect, please check again")
        else:
            flash("The user don't exist")
        
        return redirect(url_for('index'))
    return render_template('login.html', **context)

# flask-login methods

#Method to obtain and charge the data of the current user session
@login_manager.user_loader
def load_user(username):
    return UserModel.query(username)

# Function to signup new users
@app.route('/signup', methods = ['GET', 'POST'])
def signup():
    signup_form = LoginForm()
    context = {
        'signup_form': signup_form
    }
    
    if signup_form.validate_on_submit(): # if the data submit correctly
        username = signup_form.username.data #obtain the variables
        password = signup_form.password.data
        
        user_doc = get_user_by_id(username) # user_doc obtain all data of the user
        
        if user_doc.to_dict() is None: # if is empty the information of the user 
            password_hash = generate_password_hash(password) # Generate a hash password
            user_data = UserData(username, password_hash) # we create a new object user with the data
            user_put(user_data)
            
            user = UserModel(user_data)
            
            login_user(user)
            
            flash("Welcome!")
            
            return redirect(url_for('hello'))
        else:
            flash('The user exist!')
    
    return  render_template('signup.html', **context)

# Function to logout from the session if already have sign in
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Succes Logout, come back soon")
    return redirect(url_for('login'))
    
# run app
if __name__ == "__main__": # if the file is explicit execute the server run
    app.run(port = 5500, host = "0.0.0.0", debug = True)
    