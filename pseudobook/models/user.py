from passlib.apps import custom_app_context as pwd_context

from pseudobook.database import mysql, MySQL

class User():
    #LoginManager attributes
    is_active = True
    is_authenticated = True
    is_anonymous = False

    def __init__(self, userID, firstName, lastName, email, password_hash):
        self.userID = userID
        self.firstName = firstName
        self.lastName = lastName
        self.email = email
        self.password_hash = password_hash

    def __repr__(self):
        return ('{{id: {}, name: {} {}}}').format(
                self.userID,
                self.firstName,
                self.lastName
        )

    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

    @staticmethod
    def get_user_by_id(userID):
        cur = mysql.connection.cursor()
        cur.execute('''SELECT U.userID, U.firstName, U.lastName, U.email, U.passwordHash
                        FROM User AS U
                        WHERE U.userID = %s''' % (userID))
        user = cur.fetchone()
        return user

    @staticmethod
    def get_user_by_email(email):
        cur = mysql.connection.cursor()
        cur.execute('''SELECT U.userID, U.firstName, U.lastName, U.email, U.passwordHash
                        FROM User AS U
                        WHERE U.email = "%s"''' % (email))
        user = cur.fetchone()
        return user

    @staticmethod
    def register_user(firstName, lastName, email, password):
        password_hash = User.hash_password(password)

        cur = mysql.connection.cursor()
        try:
            cur.callproc('registerUser', (firstName, lastName, email, password_hash, None, None, None, None, None, None, None))
            return User(cur.lastrowid, firstName, lastName, email, password_hash)
        except (mysql.connection.Error, mysql.connection.Warning) as e:
            raise

    def get_id(self):
        return self.userID
        
'''
author @roman
'''