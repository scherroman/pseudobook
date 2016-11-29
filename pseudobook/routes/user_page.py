from flask import Blueprint, abort
from flask import render_template, url_for, request, redirect 
from flask_login import login_required, current_user

from pseudobook.database import mysql

from pseudobook.models import user as user_model

'''
Setup Blueprint
'''
mod = Blueprint('user_page', __name__, template_folder='../templates/user_page')

'''
Routes
'''
@mod.route('/user/<string:userID>', methods=['GET'])
def user_page(userID):
	user = user_model.User.get_user_by_id(userID)
	if user:
		return render_template('user_page.html', current_user=current_user, user=user)
	else:
		abort(404)