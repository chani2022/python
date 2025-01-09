import bcrypt

class PasswordManager:

    @classmethod
    def hashPassword(self, plain_password):
        bytes = plain_password.encode("utf-8")
        salt = bcrypt.gensalt()

        return bcrypt.hashpw(bytes, salt)
    
    @classmethod
    def checkPassword(self, user_plain_password, user_hash_password):
        user_bytes = user_plain_password.encode("utf-8")

        return bcrypt.checkpw(user_bytes, user_hash_password.encode("utf-8")) 