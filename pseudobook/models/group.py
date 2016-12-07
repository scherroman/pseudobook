from pseudobook.database import mysql, MySQL

class Group():
    
    def __init__(self, groupName, groupType, ownerID):
        self.groupName = groupName
        self.groupType = ownerID
        self.ownerID = ownerID

    def __repr__(self):
        return ('{{groupName: {}, groupType: {}, ownerID: {}}}').format(
                self.groupName,
                self.groupType,
                self.ownerID
        )

    @staticmethod
    def group_names(userID):

        cursor = mysql.connection.cursor()
            # cursor.execute('''SELECT U.userID, U.firstName, U.lastName
            #               FROM User AS U
            #               WHERE U.firstName LIKE \'{0}%\' 
            #                     OR U.lastName LIKE \'{0}%\' 
            #                     OR CONCAT(U.firstName, \' \', U.lastName) LIKE \'{0}%\'
            #               ORDER BY U.firstName
            #               LIMIT {1} OFFSET {2}
            #               '''.format(search, num_users, offset * num_users))
        query = '''SELECT G.groupName AS group_name
                          FROM GroupUsers GU, `Group` G
                          WHERE GU.userID = {} AND G.groupID = GU.groupID
                          '''.format(userID)
        # print(query)
        cursor_return = cursor.execute(query)
        # print(cursor_return)
        results = cursor.fetchall()
        # print(results)
        # list_of_names = results.get('list_of_names')
        list_of_names = ('\n'.join(s['group_name'] for s in results))
        # print(list_of_names)
        return list_of_names

'''
author @edgar
'''

   