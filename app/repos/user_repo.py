class UserRepo(object):
    def __init__(self, db_name, db_client):
        self._db_name = db_name
        self._db_client = db_client

    def get_all_users(self):
        db = self._db_client[self._db_name]

        user_collection = db['users']

        users = user_collection.find()
        return users