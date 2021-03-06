from pseudobook.database import mysql, MySQL

from pseudobook.models import user as user_model

class Group():
	
	def __init__(self, groupID, groupName, ownerID):
		self.groupID = groupID
		self.groupName = groupName
		self.ownerID = ownerID

	def __repr__(self):
		return ('{{groupId: {}, groupName: {}, ownerID: {}}}').format(
				self.groupID,
				self.groupName,
				self.ownerID
		)

	def create_group(self):
		cursor = mysql.connection.cursor()
		try:
			cursor.execute('''CALL createGroup(@groupID, "{}", NULL, "{}")
							  '''.format(self.groupName, self.ownerID))
			mysql.connection.commit()
			cursor.execute('''SELECT @groupID''')
		except (mysql.connection.Error, mysql.connection.Warning) as e:
			raise
		else:
			result = cursor.fetchone()
			groupID = result.get('@groupID') if result else None
			
		return groupID

	def is_member(self, userID):
		cursor = mysql.connection.cursor()
		cursor.execute('''SELECT 1 
						  FROM GroupUsers AS GU 
						  WHERE GU.groupID = {0} 
						  AND GU.userID = {1}
		                  '''.format(self.groupID, userID))
		exists = cursor.fetchone()
		
		return True if exists else False

	def is_owner(self, userID):
		return self.ownerID == userID

	def join_group(self, userID):
		cursor = mysql.connection.cursor()
		try:
			cursor.execute('''CALL joinGroup("{}", "{}")
							  '''.format(userID, self.groupID))
			mysql.connection.commit()
		except (mysql.connection.Error, mysql.connection.Warning) as e:
			raise

	def unjoin_group(self, userID):
		cursor = mysql.connection.cursor()
		try:
			cursor.execute('''CALL unjoinGroup("{}", "{}")
							  '''.format(userID, self.groupID))
			mysql.connection.commit()
		except (mysql.connection.Error, mysql.connection.Warning) as e:
			raise

	def scroll_users(self, offset, num_users, search):
		search = search if search else ""
		users = []

		cursor = mysql.connection.cursor()
		cursor.execute('''SELECT U.userID, U.firstName, U.lastName
		                  FROM GroupUsers AS GU, User AS U
		                  WHERE GU.userID = U.userID
		                        AND GU.groupID = {0} 
		                  ORDER BY U.firstName
		                  LIMIT {1} OFFSET {2}
		                  '''.format(self.groupID, num_users, offset * num_users))
		results = cursor.fetchall()

		for result in results:
		    user = user_model.User.user_from_dict(result) if result else None
		    users.append(user)

		return users

	def count_users(self, search):
		search = search if search else ""

		cursor = mysql.connection.cursor()
		cursor.execute('''SELECT COUNT(*) AS count
		                  FROM GroupUsers AS GU
		                  WHERE GU.groupID = {0}
		                  '''.format(self.groupID))
		results = cursor.fetchone()
		count = results.get('count')

		return count

	def scroll_addable_users(self, offset, num_users):
		users = []

		cursor = mysql.connection.cursor()
		cursor.execute('''SELECT U.userID, U.firstName, U.lastName
		                  FROM User AS U
		                  WHERE NOT EXISTS (SELECT 1 
							                FROM GroupUsers AS GU 
							                WHERE GU.groupID = {0}
							                AND GU.userID = U.userID)
		                  ORDER BY U.firstName
		                  LIMIT {1} OFFSET {2}
		                  '''.format(self.groupID, num_users, offset * num_users))
		results = cursor.fetchall()

		for result in results:
		    user = user_model.User.user_from_dict(result) if result else None
		    users.append(user)

		return users

	def count_addable_users(self):
		cursor = mysql.connection.cursor()
		cursor.execute('''SELECT COUNT(*) AS count
		                  FROM User AS U
		                  WHERE NOT EXISTS (SELECT 1 
							                FROM GroupUsers AS GU 
							                WHERE GU.groupID = {0}
							                AND GU.userID = U.userID)
		                  '''.format(self.groupID))
		results = cursor.fetchone()
		count = results.get('count')

		return count

	@staticmethod
	def get_group_by_id(groupID):
	    cursor = mysql.connection.cursor()
	    cursor.execute('''SELECT G.groupID, G.groupName, G.ownerID
	                      FROM `Group` AS G
	                      WHERE G.groupID = {}
	                      '''.format(groupID))
	    result = cursor.fetchone()
	    group = Group.group_from_dict(result) if result else None

	    return group

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
	def scroll_groups_for_user(userID, offset, num_groups):
	    cursor = mysql.connection.cursor()
	    query = '''SELECT G.groupName, G.groupID, G.ownerID
	                      FROM GroupUsers GU, `Group` G
	                      WHERE GU.userID = {0} AND G.groupID = GU.groupID
	                      ORDER BY G.groupName ASC
	                      LIMIT {1} OFFSET {2}
	                      '''.format(userID, num_groups, offset * num_groups)
	    cursor_return = cursor.execute(query)
	    results = cursor.fetchall()
	    return [tup for tup in (x for x in results)]

	@staticmethod
	def count_groups_for_user(userID):
	    cursor = mysql.connection.cursor()
	    cursor.execute('''SELECT COUNT(*) AS count
	                      FROM GroupUsers GU, `Group` G
	                      WHERE GU.userID = {0} AND G.groupID = GU.groupID
	                      '''.format(userID))
	    results = cursor.fetchone()
	    return results['count']

	@staticmethod
	def group_from_dict(g_dict):
		return Group(g_dict.get('groupID'), 
					 g_dict.get('groupName'),
					 g_dict.get('ownerID'))

'''
author @edgar
'''

   