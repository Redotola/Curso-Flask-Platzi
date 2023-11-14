from flask_login import UserMixin
from services.fire_store_service import get_user_by_id

# class of the user data
class UserData():
    # initialize the object
    def __init__(self, username, password):
        '''
        param data of the user
        '''
        self.username = username
        self.password = password

# class of the user inherits UserMixin
class UserModel(UserMixin):
    def __init__(self, user_data):
        """
        param user_data: UserData
        """
        self.id = user_data.username
        self.password = user_data.password
        
    # method query thta get the user data
    @staticmethod
    def query(user_id):
        user_doc = get_user_by_id(user_id)
        user_data = UserData(
            username = user_doc.id,
            password = user_doc.to_dict()['password']
        )
    
        return UserModel(user_data)