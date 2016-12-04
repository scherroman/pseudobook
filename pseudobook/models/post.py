from pseudobook.database import mysql, MySQL

from pseudobook.models import user as user_model

class Post():
 
    def __init__(self, postID, pageID, postDate, postContent, authorID):
        self.postID = postID
        self.pageID = pageID
        self.postDate = postDate
        self.postContent = postContent
        self.authorID = authorID

    def __repr__(self):
        return ('{{id: {}, pageID: {}, postDate:{}, postContent:{}, authorID:{}}}').format(
                self.postID,
                self.pageID,
                self.postDate,
                self.postContent,
                self.authorID
        )

    def get_author_name(self):
        cursor = mysql.connection.cursor()
        cursor.execute('''SELECT CONCAT(U.firstName, \' \', U.lastName) AS name
                          FROM User AS U
                          WHERE U.userID = {}
                          '''.format(self.authorID))
        result = cursor.fetchone()
        author_name = result.get('name') if result else None

        return author_name

    @staticmethod
    def get_post_by_id(postID):
        cursor = mysql.connection.cursor()
        cursor.execute('''SELECT P.postID, P.pageID, P.postDate, P.postContent, P.authorID
                          FROM Post AS P
                          WHERE P.postID = {}
                          '''.format(postID))
        result = cursor.fetchone()
        post = Post.post_from_dict(result) if result else None

        return post
        
    @staticmethod
    def post_from_dict(p_dict):
        return Post(p_dict.get('postID'), 
                    p_dict.get('pageID'),
                    p_dict.get('postDate'),
                    p_dict.get('postContent'),
                    p_dict.get('authorID'))
        
'''
author @roman
'''