# Course-Flask-Platzi
In this course I learn about the Micro Framework "Flask" that is really useful web tool

# Create environment
virtualenv "name"

# Install the packages
pip install -r requirements

# Create the terminal variable to run application
( Linux )
export FLASK_APP=app.py

( Windows )
set FLASK_APP=app.py

# Verify the variable was created
( Linux )
echo $FLASK_APP

( Windows )
echo FLASK_APP

# Run the server 
flask run

# Activate Envireonment Development
( Linux )
export FLASK_ENV=development

( Windows )
set FLASK_ENV=development