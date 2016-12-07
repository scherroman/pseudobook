from pseudobook.database import mysql, MySQL

class Group():
    
    def __init__(self, groupID, groupName, groupType, ownerID):
        self.groupID = groupID
        self.groupName = groupName
        self.groupType = ownerID
        self.ownerID = ownerID

    def __repr__(self):
        return ('{{groupName: {}, groupType: {}, ownerID: {}}}').format(
                self.groupName,
                self.groupType,
                self.ownerID
        )

    def create_group(self):
        cursor = mysql.connection.cursor()
        try:
            cursor.execute('''CALL createGroup(@groupID, "{}", "{}", "{}")
                              '''.format(self.groupName, self.groupType, self.ownerID))
            mysql.connection.commit()
            cursor.execute('''SELECT @groupID''')
        except (mysql.connection.Error, mysql.connection.Warning) as e:
            raise
        else:
            result = cursor.fetchone()
            groupID = result.get('@groupID') if result else None
            
        return groupID


    @staticmethod
    def group_names(userID):

        cursor = mysql.connection.cursor()
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

   