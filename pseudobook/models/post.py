from pseudobook.database import mysql, MySQL

from pseudobook.models import user as user_model
from pseudobook.models import comment as comment_model

class Post():
 
    def __init__(self, postID, pageID, postDate, postContent, authorID):
        self.postID = postID
        self.pageID = pageID
        self.postDate = postDate
        self.postContent = postContent
        self.authorID = authorID

    def __repr__(self):
        return ('{{postID: {}, pageID: {}, postDate:{}, postContent:{}, authorID:{}}}').format(
                self.postID,
                self.pageID,
                self.postDate,
                self.postContent,
                self.authorID
        )

    def get_comments(self):
        comments = []

        cursor = mysql.connection.cursor()
        cursor.execute('''SELECT C.commentID, C.postID, C.commentDate, C.content, C.authorID, CONCAT(U.firstName, \' \', U.lastName) AS author_name
                          FROM Comment AS C, User AS U
                          WHERE C.authorID = U.userID
                                AND C.postID = {0}
                          ORDER BY C.commentDate DESC
                          '''.format(self.postID))
        results = cursor.fetchall()

        for result in results:
            comment = comment_model.Comment.comment_from_dict(result) if result else None
            comment.author_name = result.get('author_name')
            comments.append(comment)

        return comments

    def make_comment(self, content, authorID):
        cursor = mysql.connection.cursor()
        try:
            cursor.execute('''CALL makeComment(@commentID, "{}", NOW(), "{}", "{}")
                              '''.format(self.postID, content, authorID))
            mysql.connection.commit()
            cursor.execute('''SELECT @commentID''')
        except (mysql.connection.Error, mysql.connection.Warning) as e:
            raise
        else:
            result = cursor.fetchone()
            commentID = result.get('@commentID') if result else None
            
        return commentID

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
    def remove_post(postID):
        cursor = mysql.connection.cursor()
        try:
            cursor.execute('''CALL removePost("{}")
                            '''.format(postID))
            mysql.connection.commit()
        except (mysql.connection.Error, mysql.connection.Warning) as e:
            raise
        
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