from flask import Blueprint, abort
from flask import render_template, url_for, request, redirect 
from flask_login import login_required, current_user
import json

from pseudobook.database import mysql

from pseudobook.models import user as user_model
from pseudobook.models import page as page_model
from pseudobook.models import post as post_model
from pseudobook.models import group as group_model
from pseudobook.models import advertisement as ads_model
from pseudobook.models import sale as sales_model

from pseudobook.forms.make_post import MakePost as MakePostForm
from pseudobook.forms.remove_post import RemovePost as RemovePostForm

POSTS_PER_PAGE = 10
USERS_PER_PAGE = 15
GROUPS_PER_PAGE = 15
ADS_PER_PAGE = 5
TRANSACTIONS_PER_PAGE = 15

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
	posts_offset = request.values.get('posts_offset')
	posts_offset = int(posts_offset) if posts_offset else 0
	groups_offset = request.values.get('groups_offset')
	groups_offset = int(groups_offset) if groups_offset else 0

	user = user_model.User.get_user_by_id(userID)
	if user:
		page = page_model.Page.get_page_by_user_id(userID)

		total_posts = page.count_posts(None)
		posts = page.scroll_posts(posts_offset, POSTS_PER_PAGE, None)
		prev_posts = True if posts_offset > 0 else False
		next_posts = True if ((posts_offset + 1) * POSTS_PER_PAGE) < total_posts else False

		total_groups = group_model.Group.count_groups_for_user(userID)
		groups = group_model.Group.scroll_groups_for_user(userID, groups_offset, GROUPS_PER_PAGE)
		prev_groups = True if groups_offset > 0 else False
		next_groups = True if ((groups_offset + 1) * GROUPS_PER_PAGE) < total_groups else False

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
								posts_offset=posts_offset,
								groups=groups,
								prev_groups=prev_groups,
								next_groups=next_groups,
								groups_offset=groups_offset,
								is_current_users_page=(current_user.userID == user.userID),
								make_post_form=make_post_form)
	else:
		abort(404)

@mod.route('/users', methods=['GET'])
@login_required
def users():
	users_offset = request.values.get('users_offset')
	users_offset = int(users_offset) if users_offset else 0
	user_posts_offset = request.values.get('user_posts_offset')
	user_posts_offset = int(user_posts_offset) if user_posts_offset else 0

	total_users = user_model.User.count_users(None)
	users = user_model.User.scroll_users(users_offset, USERS_PER_PAGE, None)
	prev_users = True if users_offset > 0 else False
	next_users = True if ((users_offset + 1) * USERS_PER_PAGE) < total_users else False

	# Scroll all posts made by user
	total_user_posts = page_model.Page.count_posts_for_page_type(page_model.Page.PAGE_TYPE_USER, None)
	user_posts = page_model.Page.scroll_posts_for_user_pages(user_posts_offset, POSTS_PER_PAGE, None)
	prev_user_posts = True if user_posts_offset > 0 else False
	next_user_posts = True if ((user_posts_offset + 1) * POSTS_PER_PAGE) < total_user_posts else False

	for user_post in user_posts:
			user_post.remove_post_form = RemovePostForm()
	return render_template('users.html', 
							current_user=current_user, 
							users=users, 
							prev_users=prev_users, 
							next_users=next_users,
							users_offset=users_offset,
							user_posts=user_posts,
							prev_user_posts=prev_user_posts,
							next_user_posts=next_user_posts,
							user_posts_offset=user_posts_offset)

@mod.route('/shop', methods=['GET'])
@login_required
def shop():
	searchable_columns = [c for c in ads_model.searchable_columns.keys() if not c == 'Posted By']
	user_accounts = user_model.User.get_user_accounts(current_user.userID)

	return render_template('shop.html',
		searchable_columns=searchable_columns,
		user_accounts=user_accounts)

@mod.route('/accounthistory', methods=['GET'])
@login_required
def accounthistory():
	user_accounts = user_model.User.get_user_accounts(current_user.userID)

	return render_template('accounthistory.html',
		user_accounts=user_accounts)

'''
Post Methods
'''
@mod.route('/shop/getallitems', methods=['POST'])
@login_required
def getallitems():
    searchcol = request.json['searchcol']
    search = request.json['search']

    ads = ads_model.Advertisement.scroll_ads(0, ADS_PER_PAGE, searchcol, search, "", "")
    return json.dumps([o.__dict__ for o in ads])

@mod.route('/shop/getsuggesteditems', methods=['POST'])
@login_required
def getsuggesteditems():
    searchcol = request.json['searchcol']
    search = request.json['search']

    ads = ads_model.Advertisement.get_suggestions_for_user(0, ADS_PER_PAGE, current_user.userID, searchcol, search)
    return json.dumps([o.__dict__ for o in ads])

@mod.route('/shop/getbestsellers', methods=['POST'])
@login_required
def getbestsellers():
    searchcol = request.json['searchcol']
    search = request.json['search']

    ads = ads_model.Advertisement.get_best_sellers(0, ADS_PER_PAGE, searchcol, search)
    return json.dumps([o.__dict__ for o in ads])

@mod.route('/user/getaccounthistory', methods=['POST'])
@login_required
def getaccounthistory():
    accountNumber = request.json['accountNumber']

    history = sales_model.Sale.get_user_account_history(0, TRANSACTIONS_PER_PAGE, current_user.userID, accountNumber)
    return json.dumps([o.__dict__ for o in history])

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

	remove_post_form = RemovePostForm(request.form)
	if request.form and remove_post_form.validate_on_submit():
		# Only allow user who owns page to delete a post on that page
		post = post_model.Post.get_post_by_id(postID)
		page = page_model.Page.get_page_by_id(post.pageID)
		if page.pageType == page_model.Page.PAGE_TYPE_USER:
			if current_user.userID == page.userID or current_user.userID == post.authorID:
				try:
					post_model.Post.remove_post(postID)
				except (mysql.connection.Error, mysql.connection.Warning) as e:
				    print(e)
				    # Print custom error message
				    if e.args[0] == 1644:
				        flash(e.args[1])
				    else:
				        flash('There was an error removing this post.')
			else:
				abort(403)
	else:
		flash('There was an error removing this post.')

	return redirect(request.referrer)
	