# Course-Flask-Platzi
In this course I learn about the Micro Framework "Flask" that is really useful web tool to create web applications with Python

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

# Activate Environment Development
( Linux )
export FLASK_ENV=development

( Windows )
set FLASK_ENV=development

# Google Cloud commands CLI
- Verify if the gcloud instance is already installed

find gcloud

- Initialize the console command

gcloud init

- Run the login in browser

gcloud auth login 

# Create a project in Google Cloud console
<img src = "https://github.com/Redotola/Curso-Flask-Platzi/blob/main/assets/gcloud.png">

<img src = "https://github.com/Redotola/Curso-Flask-Platzi/blob/main/assets/gcloud1.png">

<img src = "https://github.com/Redotola/Curso-Flask-Platzi/blob/main/assets/gcloud2.png">

<img src = "https://github.com/Redotola/Curso-Flask-Platzi/blob/main/assets/gcloud3.png">

<img src = "https://github.com/Redotola/Curso-Flask-Platzi/blob/main/assets/gcloud4.png">

<img src = "https://github.com/Redotola/Curso-Flask-Platzi/blob/main/assets/gcloud5.png">

<img src = "https://github.com/Redotola/Curso-Flask-Platzi/blob/main/assets/gcloud6.png">

<img src = "https://github.com/Redotola/Curso-Flask-Platzi/blob/main/assets/gcloud7.png">

# Set the ID project to access base
<!-- Set the environment variable of the Google cloud project -->
( Linux ) export GOOGLE_CLOUD_PROJECT='ID'
( Windows ) set GOOGLE_CLOUD_PROJECT='ID' 

or 

<!-- Command to set the project ID in the gcloud CLI -->
( Windows ) gcloud auth application-default set-quota-project "ID of the project"