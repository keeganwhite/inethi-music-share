from passlib.apps import custom_app_context


class MusicShareAPIAuth:
    """
        Class used for password handling for the API
    """

    @staticmethod
    def hash_password(userModel, password):
        """ Takes a users plaintext password and saves the hashed password

        :param userModel: instance of the user model
        :param password: plaintext password
        """
        userModel.password_hash = custom_app_context.encrypt(password)

    @staticmethod
    def verify_password(password, hash_to_compare):
        """ Verifies the users hashed password

        :param hash_to_compare:
        :param password: plaintext password
        :return: true if the password is correct and false if it is not
        """
        return custom_app_context.verify(str(password), hash_to_compare)