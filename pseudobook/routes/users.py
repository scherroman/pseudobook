from flask import Blueprint, abort
from flask import render_template, url_for, request, redirect 
from flask_login import login_required, current_user

from pseudobook.database import mysql

from pseudobook.models import user as user_model

USERS_PER_PAGE = 15

'''
Setup Blueprint
'''
mod = Blueprint('users', __name__, template_folder='../templates/users')

'''
Routes
'''
@mod.route('/user/<string:userID>', methods=['GET'])
@login_required
def user_page(userID):
	user = user_model.User.get_user_by_id(userID)
	if user:
		return render_template('user_page.html', current_user=current_user, user=user)
	else:
		abort(404)

@mod.route('/users', methods=['GET'])
@login_required
def users():
	offset = request.values.get('offset')
	offset = int(offset) if offset else 0
	search = request.values.get('search')

	print("search: {}".format(search))

	total_users = user_model.User.count_users(search)
	users = user_model.User.scroll_users(offset, USERS_PER_PAGE, search)
	prev_users = True if offset > 0 else False
	next_users = True if ((offset + 1) * USERS_PER_PAGE) < total_users else False

	return render_template('users.html', 
							current_user=current_user, 
							users=users, 
							prev=prev_users, 
							next=next_users,
							offset=offset,
							search=search)