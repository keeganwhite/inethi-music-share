
class User:
    """
        Class used for user and password handling for inethi-musicshare-api
    """
    def __init__(self, username):
        self.username = username
        self.password_hash = ""
