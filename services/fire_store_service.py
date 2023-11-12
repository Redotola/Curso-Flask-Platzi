import firebase_admin # import the firebase library that allow us to create a connection with the database in Google Cloud
from firebase_admin import credentials
from firebase_admin import firestore

project_id = 'flask-platzi-firebase'
credential = credentials.ApplicationDefault()
firebase_admin.initialize_app(credential, {'projectId': project_id})

db = firestore.client()

def get_users():
    return db.collection('users').get()