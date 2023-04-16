class UserService(object):
    def __init__(self, user_repo):
        self._user_repo = user_repo

    def get_all_users(self):
        users = self._user_repo.get_all_users()
        for user in users:
            print(user)