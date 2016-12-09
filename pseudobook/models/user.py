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
        return ('{{userId: {}, firstName: {}, lastName {}}}').format(
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
            cursor.execute('''CALL registerUser(@userID, "{}", "{}", "{}", "{}", NULL, NULL, NULL, NULL, NULL, NULL, NULL)
                              '''.format(self.firstName, self.lastName, self.email, self.password_hash))
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
                          WHERE U.userID = {}
                          '''.format(userID))
        result = cursor.fetchone()
        user = User.user_from_dict(result) if result else None

        return user

    @staticmethod
    def get_user_by_email(email):
        cursor = mysql.connection.cursor()
        cursor.execute('''SELECT U.userID, U.firstName, U.lastName, U.email, U.passwordHash
                          FROM User AS U
                          WHERE U.email = "{}"
                          '''.format(email))
        result = cursor.fetchone()
        user = User.user_from_dict(result) if result else None

        return user

    @staticmethod
    def get_user_accounts(userID):
        cursor = mysql.connection.cursor()
        cursor.execute('''SELECT A.accountNumber, A.creditCardNumber
                          FROM UserAccounts A
                          WHERE A.userID = {0}
                          '''.format(userID))
        results = cursor.fetchall()
        
        accounts = []
        for result in results:
            accounts.append((result.get('accountNumber'), result.get('creditCardNumber')))
            
        return accounts

    @staticmethod
    def scroll_users(offset, num_users, search):
        search = search if search else ""
        users = []
        
        cursor = mysql.connection.cursor()
        cursor.execute('''SELECT U.userID, U.firstName, U.lastName
                          FROM User AS U
                          WHERE U.firstName LIKE \'{0}%\' 
                                OR U.lastName LIKE \'{0}%\' 
                                OR CONCAT(U.firstName, \' \', U.lastName) LIKE \'{0}%\'
                          ORDER BY U.firstName
                          LIMIT {1} OFFSET {2}
                          '''.format(search, num_users, offset * num_users))
        results = cursor.fetchall()
        
        for result in results:
            user = User.user_from_dict(result) if result else None
            users.append(user)

        return users

    @staticmethod
    def count_users(search):
        search = search if search else ""

        cursor = mysql.connection.cursor()
        cursor.execute('''SELECT COUNT(*) AS count
                          FROM User AS U
                          WHERE U.firstName LIKE \'{0}%\' 
                                OR U.lastName LIKE \'{0}%' 
                                OR CONCAT(U.firstName, \' \', U.lastName) LIKE \'{0}\'
                          '''.format(search))
        results = cursor.fetchone()
        count = results.get('count')

        return count

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