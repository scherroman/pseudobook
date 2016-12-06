from flask import Blueprint, abort
from flask import render_template, url_for, request, redirect 
from flask_login import login_required, current_user

from pseudobook.database import mysql

from pseudobook.models import user as user_model
from pseudobook.models import page as page_model
from pseudobook.models import post as post_model

from pseudobook.forms.make_post import MakePost as MakePostForm
from pseudobook.forms.remove_post import RemovePost as RemovePostForm

POSTS_PER_PAGE = 10
USERS_PER_PAGE = 15

'''
Setup Blueprint
'''
mod = Blueprint('users', __name__, template_folder='../templates/users')

'''
View Routes
'''
@mod.route('/user/<string:userID>', methods=['GET'])
@login_required
def user_page(userID):
	search = request.values.get('search')
	offset = request.values.get('offset')
	offset = int(offset) if offset else 0

	user = user_model.User.get_user_by_id(userID)
	if user:
		page = page_model.Page.get_page_by_user_id(userID)

		total_posts = page.count_posts(search)
		posts = page.scroll_posts(offset, POSTS_PER_PAGE, search)
		prev_posts = True if offset > 0 else False
		next_posts = True if ((offset + 1) * POSTS_PER_PAGE) < total_posts else False

		groups = []
		prev_groups = None
		next_groups = None

		make_post_form = MakePostForm()
		for post in posts:
			remove_post_form = RemovePostForm()
			post.remove_post_form = remove_post_form
		return render_template('user_page.html', 
								current_user=current_user, 
								user=user,
								page=page,
								posts=posts,
								prev_posts=prev_posts, 
								next_posts=next_posts,
								offset=offset,
								search=search,
								groups=groups,
								is_current_users_page=(current_user.userID == user.userID),
								make_post_form=make_post_form)
	else:
		abort(404)

@mod.route('/users', methods=['GET'])
@login_required
def users():
	search = request.values.get('search')
	offset = request.values.get('offset')
	offset = int(offset) if offset else 0
	user_post_offset = request.values.get('user_post_offset')
	user_post_offset = int(user_post_offset) if user_post_offset else 0

	total_users = user_model.User.count_users(search)
	users = user_model.User.scroll_users(offset, USERS_PER_PAGE, search)
	prev_users = True if offset > 0 else False
	next_users = True if ((offset + 1) * USERS_PER_PAGE) < total_users else False

	# Scroll all posts made by user
	total_user_posts = page_model.Page.count_posts_for_page_type(page_model.Page.PAGE_TYPE_USER, None)
	user_posts = page_model.Page.scroll_posts_for_user_pages(user_post_offset, POSTS_PER_PAGE, None)
	prev_user_posts = True if user_post_offset > 0 else False
	next_user_posts = True if ((user_post_offset + 1) * POSTS_PER_PAGE) < total_user_posts else False

	for user_post in user_posts:
			remove_post_form = RemovePostForm()
			user_post.remove_post_form = remove_post_form
	return render_template('users.html', 
							current_user=current_user, 
							users=users, 
							prev_users=prev_users, 
							next_users=next_users,
							offset=offset,
							search=search,
							user_posts=user_posts,
							prev_user_posts=prev_user_posts,
							next_user_posts=next_user_posts,
							user_post_offset=user_post_offset)
'''
Form Routes
'''
@mod.route('/users/forms/make_post', methods=['POST'])
@login_required
def make_post_form():
	content = request.form['content']
	pageID = request.form['pageID']
	authorID = current_user.userID
	page = page_model.Page.get_page_by_id(pageID)

	make_post_form = MakePostForm(request.form)
	if request.form and make_post_form.validate_on_submit():
		try:
			page.post_to_page(content, authorID)
		except (mysql.connection.Error, mysql.connection.Warning) as e:
			print(e)
			flash('There was an error posting to this page.')
	else:
		flash('There was an error posting to this page.')

	return redirect(request.referrer)

@mod.route('/users/forms/remove_post', methods=['POST'])
@login_required
def remove_post_form():
	postID = request.form['postID']

	# Only allow user who owns page to delete a post on that page
	post = post_model.Post.get_post_by_id(postID)
	page = page_model.Page.get_page_by_id(post.pageID)
	if page.pageType == page_model.Page.PAGE_TYPE_USER:
		if current_user.userID == page.userID or current_user.userID == post.authorID:
			page.remove_post(postID)
		else:
			abort(403)

	return redirect(request.referrer)
	