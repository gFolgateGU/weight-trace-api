from app.models.user import User

class UserRepo(object):
    def __init__(self, db_name, db_client):
        self._db_name = db_name
        self._db_client = db_client

    def get_all_users(self):
        db = self._db_client[self._db_name]

        user_collection = db['users']

        users = user_collection.find()

        if users:
            for user in users:
                user_model = User(**user)
        
        return None

    def get_user_by_username(self, username: str):
        db = self._db_client[self._db_name]

        user_collection = db['users']

        user = user_collection.find_one({"usersname": username})

        if user:
            user_model = User(**user)
            return user_model

        return None