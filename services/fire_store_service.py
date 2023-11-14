import firebase_admin # import the firebase library that allow us to create a connection with the database in Google Cloud
from firebase_admin import credentials
from firebase_admin import firestore

credential = credentials.ApplicationDefault()
firebase_admin.initialize_app(credential)

db = firestore.client()

def get_users():
    return db.collection('users').get()

def get_user_by_id(user_id):
    return db.collection('users').document(user_id).get()

def get_todos(user_id):
    return db.collection('users').document(user_id).collection('todos').get()

def user_put(user_data):
    user_ref = db.collection('users').document(user_data.username)
    user_ref.set({'password': user_data.password})
    
def put_todo(user_id, description):
    todos_collection_ref = db.collection('users').document(user_id).collection('todos')
    todos_collection_ref.add({'description': description, 'done': False})
    
def delete_todo(user_id, todo_id):
    todo_ref = _get_todo_ref(user_id, todo_id)
    todo_ref.delete()
    
def update_todo(user_id, todo_id, done):
    todo_done = not bool(done)
    todo_ref = _get_todo_ref(user_id, todo_id)
    todo_ref.update({'done': todo_done})

def _get_todo_ref(user_id, todo_id):
    return db.document(f'users/{user_id}/todos/{todo_id}')