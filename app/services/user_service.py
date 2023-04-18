class UserService(object):
    def __init__(self, user_repo):
        self._user_repo = user_repo

    def register_user(self, username, password):
        # Create a new user object with the passed in info
        pass
    
    def verify_user(self, username, password):
        # Retrieve the user from the db
        user = self._user_repo.get_user_by_username(username)

        # Verify that the user exists in the DB
        if not user:
            return False
        
        # If user exists, verify the password
        user_ok = user.verify_password(password)

        # If the password is okay, then give the greenlight
        if user_ok:
            return True
        
        return False
    
    def get_all_users(self):
        users = self._user_repo.get_all_users()
        for user in users:
            print(user)