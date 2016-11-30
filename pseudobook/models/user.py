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

    def get_id(self):
        return self.userID

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

    def register_user(self): 
        cursor = mysql.connection.cursor()
        try:
            cursor.execute('''CALL registerUser(@userID, "%s", "%s", "%s", "%s", NULL, NULL, NULL, NULL, NULL, NULL, NULL)'''
                            % (self.firstName, self.lastName, self.email, self.password_hash))
            mysql.connection.commit()
            cursor.execute('''SELECT @userID''')
        except (mysql.connection.Error, mysql.connection.Warning) as e:
            raise
        else:
            result = cursor.fetchone()
            userID = result.get('@userID') if result else None
            
            return userID

    @staticmethod
    def hash_password(password):
        return pwd_context.encrypt(password)

    @staticmethod
    def get_user_by_id(userID):
        cursor = mysql.connection.cursor()
        cursor.execute('''SELECT U.userID, U.firstName, U.lastName, U.email, U.passwordHash
                        FROM User AS U
                        WHERE U.userID = %s''' % (userID))
        result = cursor.fetchone()
        user = User.user_from_dict(result) if result else None

        return user

    @staticmethod
    def get_user_by_email(email):
        cursor = mysql.connection.cursor()
        cursor.execute('''SELECT U.userID, U.firstName, U.lastName, U.email, U.passwordHash
                        FROM User AS U
                        WHERE U.email = "%s"''' % (email))
        result = cursor.fetchone()
        user = User.user_from_dict(result) if result else None

        return user

    @staticmethod
    def user_from_dict(u_dict):
        return User(u_dict.get('userID'), 
                    u_dict.get('firstName'),
                    u_dict.get('lastName'),
                    u_dict.get('email'),
                    u_dict.get('passwordHash'))
        
'''
author @roman
'''