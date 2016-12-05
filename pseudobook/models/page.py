from pseudobook.database import mysql, MySQL

from pseudobook.models import post as post_model

class Page():
    PAGE_TYPE_USER = 'pr'
    PAGE_TYPE_GROUP = 'gr'
 
    def __init__(self, pageID, userID, groupID, pageType):
        self.pageID = pageID
        self.userID = userID
        self.groupID = groupID
        self.pageType = pageType

    def __repr__(self):
        return ('{{id: {}, userID: {}, groupID: {}, pageType: {}}}').format(
                self.pageID,
                self.userID,
                self.groupID,
                self.pageType
        )

    def post_to_page(self, content, author_id):
        cursor = mysql.connection.cursor()
        try:
            cursor.execute('''CALL makePost(@postID, "{}", "{}", "{}", NOW(), "{}")
                              '''.format(author_id, self.pageID, self.pageType, content))
            mysql.connection.commit()
            cursor.execute('''SELECT @postID''')
        except (mysql.connection.Error, mysql.connection.Warning) as e:
            raise
        else:
            result = cursor.fetchone()
            postID = result.get('@postID') if result else None

        return postID

    def remove_post(self, postID):
      cursor = mysql.connection.cursor()
      try:
          cursor.execute('''CALL removePost("{}")
                            '''.format(postID))
          mysql.connection.commit()
      except (mysql.connection.Error, mysql.connection.Warning) as e:
          raise

    def scroll_posts(self, offset, num_posts, search):
        search = search if search else ""
        posts = []
        
        cursor = mysql.connection.cursor()
        cursor.execute('''SELECT P.postID, P.pageID, P.postDate, P.postContent, P.authorID, CONCAT(U.firstName, \' \', U.lastName) AS author_name
                          FROM Post AS P, User AS U
                          WHERE P.authorID = U.userID
                                AND P.pageID = {0} 
                                AND P.postContent LIKE \'%{1}%\'
                          ORDER BY P.postDate DESC
                          LIMIT {2} OFFSET {3}
                          '''.format(self.pageID, search, num_posts, offset * num_posts))
        results = cursor.fetchall()
        
        for result in results:
            post = post_model.Post.post_from_dict(result) if result else None
            post.author_name = result.get('author_name')
            posts.append(post)

        return posts

    def count_posts(self, search):
        search = search if search else ""

        cursor = mysql.connection.cursor()
        cursor.execute('''SELECT COUNT(*) AS count
                          FROM Post AS P
                          WHERE P.pageID = {0} AND P.postContent LIKE \'%{1}%\'
                          '''.format(self.pageID, search))
        results = cursor.fetchone()
        count = results.get('count')

        return count

    @staticmethod
    def get_page_by_id(pageID):
        cursor = mysql.connection.cursor()
        cursor.execute('''SELECT P.pageID, P.userID, P.groupID, P.pageType
                          FROM Page AS P
                          WHERE P.pageID = {}
                          '''.format(pageID))
        result = cursor.fetchone()
        page = Page.page_from_dict(result) if result else None

        return page

    @staticmethod
    def get_page_by_user_id(userID):
        cursor = mysql.connection.cursor()
        cursor.execute('''SELECT P.pageID, P.userID, P.groupID, P.pageType
                          FROM Page AS P
                          WHERE P.userID = {}
                          '''.format(userID))
        result = cursor.fetchone()
        page = Page.page_from_dict(result) if result else None

        return page

    @staticmethod
    def get_page_by_group_id(groupID):
        cursor = mysql.connection.cursor()
        cursor.execute('''SELECT P.pageID, P.userID, P.groupID, P.pageType
                          FROM Page AS P
                          WHERE P.groupID = {}
                          '''.format(groupID))
        result = cursor.fetchone()
        page = Page.page_from_dict(result) if result else None

        return page

    @staticmethod
    def scroll_posts_for_user_pages(offset, num_posts, search): 
        search = search if search else ""
        posts = []
        
        cursor = mysql.connection.cursor()
        cursor.execute('''SELECT P.postID, P.pageID, P.postDate, P.postContent, P.authorID, CONCAT(U.firstName, \' \', U.lastName) AS author_name, U2.userID AS page_owner_id, CONCAT(U2.firstName, \' \', U2.lastName) AS page_owner_name
                          FROM Post AS P, User AS U, Page AS Pa, User AS U2
                          WHERE Pa.pageType = '{0}'
                                AND P.authorID = U.userID
                                AND P.pageID = Pa.pageID
                                AND Pa.userID = U2.userID
                                AND P.postContent LIKE \'%{1}%\'
                          ORDER BY P.postDate DESC
                          LIMIT {2} OFFSET {3}
                          '''.format(Page.PAGE_TYPE_USER, search, num_posts, offset * num_posts))
        results = cursor.fetchall()
        
        for result in results:
            post = post_model.Post.post_from_dict(result) if result else None
            post.author_name = result.get('author_name')
            post.page_owner_id = result.get('page_owner_id')
            post.page_owner_name = result.get('page_owner_name')
            posts.append(post)

        return posts

    @staticmethod
    def count_posts_for_page_type(pageType, search):
        search = search if search else ""

        cursor = mysql.connection.cursor()
        cursor.execute('''SELECT COUNT(*) AS count
                          FROM Post AS P, Page AS Pa
                          WHERE Pa.pageType = '{0}'
                                AND P.pageID = Pa.pageID
                                AND P.postContent LIKE \'%{1}%\'
                          '''.format(pageType, search))
        results = cursor.fetchone()
        count = results.get('count')

        return count
 
    @staticmethod
    def page_from_dict(p_dict):
        return Page(p_dict.get('pageID'), 
                    p_dict.get('userID'),
                    p_dict.get('groupID'),
                    p_dict.get('pageType'))
        
'''
author @roman
'''