from app.models.user import User

class UserService(object):
    def __init__(self, user_repo):
        self._user_repo = user_repo


    def register_user(self, username, password):
        # Create a new user object with the passed in info
        
        # First make sure that the user doesn't already exist
        user = self._user_repo.get_user_by_username(username)

        # Verify that user doesn't exist
        if user:
            return False

        new_user = User.create(username, password)

        success = self._user_repo.add_user(new_user)

        return success
        
    
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