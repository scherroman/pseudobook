from pseudobook.database import mysql, MySQL

from pseudobook.models import user as user_model

class Group():
	
	def __init__(self, groupID, groupName, ownerID):
		self.groupID = groupID
		self.groupName = groupName
		self.ownerID = ownerID

	def __repr__(self):
		return ('{{groupName: {}, ownerID: {}}}').format(
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
			print("result {}".format(result))
			groupID = result.get('@groupID') if result else None

		print("groupID {}".format(groupID))
			
		return groupID

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
	def group_list(userID):
		cursor = mysql.connection.cursor()
		query = '''SELECT G.groupName, G.groupID, G.ownerID
						  FROM GroupUsers GU, `Group` G
						  WHERE GU.userID = {} AND G.groupID = GU.groupID
						  '''.format(userID)
		cursor_return = cursor.execute(query)
		results = cursor.fetchall()
		return [tup for tup in (x for x in results)]

	@staticmethod
	def group_from_dict(g_dict):
		return Group(g_dict.get('groupID'), 
					 g_dict.get('groupName'),
					 g_dict.get('ownerID'))

'''
author @edgar
'''

   