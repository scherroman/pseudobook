from pseudobook.database import mysql, MySQL

class Comment():
 
    def __init__(self, commentID, postID, commentDate, content, authorID):
        self.commentID = commentID
        self.postID = postID
        self.commentDate = commentDate
        self.content = content
        self.authorID = authorID

    def __repr__(self):
        return ('{{commentID: {}, postID: {}, commentDate:{}, content:{}, authorID:{}}}').format(
                self.commentID,
                self.postID,
                self.commentDate,
                self.content,
                self.authorID
        )

    def serialize(self):
        return {'commentID': self.commentID, 
                'postID': self.postID,
                'commentDate': self.commentDate,
                'content': self.content,
                'authorID': self.authorID }

    @staticmethod
    def get_comment_by_id(commentID):
        cursor = mysql.connection.cursor()
        cursor.execute('''SELECT C.commentID, C.postID, C.commentDate, C.content, C.authorID, CONCAT(U.firstName, \' \', U.lastName) AS author_name
                          FROM Comment AS C, User AS U
                          WHERE C.authorID = U.userID
                                AND C.commentID = {}
                          '''.format(commentID))
        result = cursor.fetchone()
        comment = Comment.comment_from_dict(result) if result else None
        comment.author_name = result.get('author_name')

        return comment

    @staticmethod
    def remove_comment(commentID):
        cursor = mysql.connection.cursor()
        try:
            cursor.execute('''CALL removeComment("{}")
                            '''.format(commentID))
            mysql.connection.commit()
        except (mysql.connection.Error, mysql.connection.Warning) as e:
            raise
        
    @staticmethod
    def comment_from_dict(c_dict):
        return Comment(c_dict.get('commentID'), 
                    c_dict.get('postID'),
                    c_dict.get('commentDate'),
                    c_dict.get('content'),
                    c_dict.get('authorID'))
        
'''
author @roman
'''