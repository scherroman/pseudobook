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
    def scroll_groups(offset, num_users, search):
        search = search if search else ""
        
        cursor = mysql.connection.cursor()
        cursor.execute('''SELECT *
                          FROM `Group` AS G
                          WHERE G.groupName LIKE \'{0}%\'
                          ORDER BY G.groupName
                          LIMIT {1} OFFSET {2}
                          '''.format(search, num_users, offset * num_users))
        results = cursor.fetchall()
        
        groups = [Group.group_from_dict(tup) for tup in (x for x in results)]

        return groups

    @staticmethod
    def group_from_dict(g_dict):
        return Group(g_dict['groupID'], 
                    g_dict['groupName'],
                    g_dict['groupType'],
                    g_dict['ownerID'])

    @staticmethod
    def count_groups(search):
        search = search if search else ""

        cursor = mysql.connection.cursor()
        cursor.execute('''SELECT COUNT(*) AS count
                          FROM `Group` AS G
                          WHERE G.groupName LIKE \'{0}%\'
                          '''.format(search))
        results = cursor.fetchone()
        return results['count']

    @staticmethod
    def group_list(userID):
        cursor = mysql.connection.cursor()
        query = '''SELECT G.groupName, G.groupID, G.ownerID
                          FROM GroupUsers GU, `Group` G
                          WHERE GU.userID = {} AND G.groupID = GU.groupID
                          '''.format(userID)
        cursor_return = cursor.execute(query)
        results = cursor.fetchall()
        return [tup for tup in (x for x in results)]

'''
author @edgar
'''

   