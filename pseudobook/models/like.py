from pseudobook.database import mysql, MySQL

class Like():
 
    def __init__(self, parentID, authorID, contentType):
        self.parentID = parentID
        self.authorID = authorID
        self.contentType = contentType

    def __repr__(self):
        return ('{{parentID: {}, authorID: {}, contentType:{}}}').format(
                self.parentID,
                self.authorID,
                self.contentType,
        )

    def serialize(self):
        return {'parentID': self.parentID, 
                'authorID': self.authorID,
                'contentType': self.contentType}

    @staticmethod
    def like(parentID, authorID, contentType):
        cursor = mysql.connection.cursor()
        cursor.execute('''CALL `like`({0}, {1}, "{2}")
                          '''.format(parentID, authorID, contentType))
        mysql.connection.commit()

    @staticmethod
    def unlike(parentID, authorID, contentType):
        cursor = mysql.connection.cursor()
        cursor.execute('''CALL unlike({0}, {1}, "{2}")
                          '''.format(parentID, authorID, contentType))
        mysql.connection.commit()

    @staticmethod
    def like_count(parentID, contentType):
        cursor = mysql.connection.cursor()
        query = '''SELECT COUNT(*) AS count
                   FROM Likes AS L 
                   WHERE L.parentID = {0}
                         AND L.contentType = "{1}"
                   '''.format(parentID, contentType)  

        cursor.execute(query)
        result = cursor.fetchone()
        count = result.get('count')

        return count

    @staticmethod
    def user_has_liked(parentID, userID, contentType):
        cursor = mysql.connection.cursor()
        #check if like or unlike
        query = '''SELECT COUNT(*) AS count
                   FROM Likes AS L 
                   WHERE L.parentID = {0}
                         AND L.authorID = {1}
                         AND L.contentType = "{2}"
                   '''.format(parentID, userID, contentType)    

        cursor.execute(query)
        result = cursor.fetchone()
        count = result.get('count')

        return False if count == 0 else True
        
    @staticmethod
    def like_from_dict(l_dict):
        return Comment(l_dict.get('parentID'), 
                    l_dict.get('authorID'),
                    l_dict.get('contentType'))
        
'''
author @roman
'''