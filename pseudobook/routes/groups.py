from flask import Blueprint, flash
from flask import render_template, url_for, request, redirect 
from flask import jsonify
from flask_login import login_required, current_user
from urllib.parse import urlparse, urljoin

from pseudobook.database import mysql

from pseudobook.models import page as page_model
from pseudobook.models import group as group_model
from pseudobook.models import page as page_model
from pseudobook.models import post as post_model

from pseudobook.forms.create_group import CreateGroup as CreateGroupForm
from pseudobook.forms.make_post import MakePost as MakePostForm
from pseudobook.forms.remove_post import RemovePost as RemovePostForm
from pseudobook.forms.join_unjoin_group import JoinUnjoinGroup as JoinUnjoinForm

POSTS_PER_PAGE = 10
USERS_PER_PAGE = 15
GROUPS_PER_PAGE = 15

'''
Setup Blueprint
'''
mod = Blueprint('groups', __name__, template_folder='../templates/groups')

'''
View Routes
'''
@mod.route('/groups', methods=['GET'])
@login_required
def groups():
    groups_offset = request.values.get('groups_offset')
    groups_offset = int(groups_offset) if groups_offset else 0
    group_posts_offset = request.values.get('group_posts_offset')
    group_posts_offset = int(group_posts_offset) if group_posts_offset else 0

    total_groups = group_model.Group.count_groups(None)
    groups = group_model.Group.scroll_groups(groups_offset, GROUPS_PER_PAGE, None)
    prev_groups = True if groups_offset > 0 else False
    next_groups = True if ((groups_offset + 1) * GROUPS_PER_PAGE) < total_groups else False

    # Scroll all posts made in groups
    total_group_posts = page_model.Page.count_posts_for_page_type(page_model.Page.PAGE_TYPE_GROUP, None)
    group_posts = page_model.Page.scroll_posts_for_group_pages(group_posts_offset, POSTS_PER_PAGE, None)
    prev_group_posts = True if group_posts_offset > 0 else False
    next_group_posts = True if ((group_posts_offset + 1) * POSTS_PER_PAGE) < total_group_posts else False

    for group_post in group_posts:
        group_post.remove_post_form = RemovePostForm()
        group_post.like_button = post_model.Post.like_button(group_post.postID, current_user.userID, "po")
        group_post.counter = post_model.Post.like_count(group_post.postID, "po")
    return render_template('groups.html', 
                            current_user=current_user, 
                            groups=groups, 
                            prev_groups=prev_groups, 
                            next_groups=next_groups,
                            groups_offset=groups_offset,
                            group_posts=group_posts,
                            prev_group_posts=prev_group_posts,
                            next_group_posts=next_group_posts,
                            group_posts_offset=group_posts_offset)

@mod.route('/group/<string:groupID>', methods=['GET'])
@login_required
def group_page(groupID):
    posts_offset = request.values.get('posts_offset')
    posts_offset = int(posts_offset) if posts_offset else 0

    users_offset = request.values.get('users_offset')
    users_offset = int(users_offset) if users_offset else 0

    addable_users_offset = request.values.get('addable_users_offset')
    addable_users_offset = int(addable_users_offset) if addable_users_offset else 0

    group = group_model.Group.get_group_by_id(groupID)
    if group:
        page = page_model.Page.get_page_by_group_id(groupID)

    total_posts = page.count_posts(None)
    posts = page.scroll_posts(posts_offset, POSTS_PER_PAGE, None)
    prev_posts = True if posts_offset > 0 else False
    next_posts = True if ((posts_offset + 1) * POSTS_PER_PAGE) < total_posts else False

    total_users = group.count_users(None)
    users = group.scroll_users(users_offset, USERS_PER_PAGE, None)
    prev_users = True if users_offset > 0 else False
    next_users = True if ((users_offset + 1) * USERS_PER_PAGE) < total_users else False

    total_addable_users = group.count_addable_users()
    addable_users = group.scroll_addable_users(addable_users_offset, USERS_PER_PAGE)
    prev_addable_users = True if addable_users_offset > 0 else False
    next_addable_users = True if ((addable_users_offset + 1) * USERS_PER_PAGE) < total_addable_users else False

    current_user_is_member = group.is_member(current_user.userID)

    make_post_form = MakePostForm()
    join_unjoin_form = JoinUnjoinForm()
    for post in posts:
        post.remove_post_form = RemovePostForm()
        post.like_button = post_model.Post.like_button(post.postID, current_user.userID, "po")
        post.counter = post_model.Post.like_count(post.postID, "po")
    for user in users:
        user.join_unjoin_form = JoinUnjoinForm()
    for user in addable_users:
        user.join_unjoin_form = JoinUnjoinForm()
    return render_template('group_page.html', 
                            current_user=current_user, 
                            group=group,
                            page=page,
                            current_user_is_member=current_user_is_member,
                            posts=posts,
                            prev_posts=prev_posts, 
                            next_posts=next_posts,
                            posts_offset=posts_offset,
                            users=users,
                            prev_users=prev_users,
                            next_users=next_users,
                            users_offset=users_offset,
                            addable_users=addable_users,
                            prev_addable_users=prev_addable_users,
                            next_addable_users=next_addable_users,
                            addable_users_offset=addable_users_offset,
                            make_post_form=make_post_form,
                            join_unjoin_form=join_unjoin_form)

@mod.route('/groups/create', methods=['GET', 'POST'])
@login_required
def create():
    create_group_form = CreateGroupForm()
    return render_template('create.html', form=create_group_form)

'''
Form Routes
'''
@mod.route('/groups/forms/create', methods=['POST'])
def create_group_form():
    groupName = request.form['groupName']

    create_group_form = CreateGroupForm(request.form)

    if request.form and create_group_form.validate_on_submit():
        new_group = group_model.Group(None, groupName, current_user.userID)
        try:
            new_group.groupID = new_group.create_group()
        except (mysql.connection.Error, mysql.connection.Warning) as e:
                print("Exeption of type {} occured: {}".format(type(e), e))
        else:
                return redirect(url_for('groups.group_page', groupID=new_group.groupID))

        return redirect(url_for('groups.create'))
    else:
        flash('There was an error in group creation. Please try again.')
        return redirect(url_for('groups.create'))

'''
Form Routes
'''
@mod.route('/groups/forms/make_post', methods=['POST'])
@login_required
def make_post_form():
    content = request.form['content']
    pageID = request.form['pageID']
    authorID = current_user.userID
    page = page_model.Page.get_page_by_id(pageID)

    make_post_form = MakePostForm(request.form)
    if request.form and make_post_form.validate_on_submit():
        try:
            postID = page.post_to_page(content, authorID)
        except (mysql.connection.Error, mysql.connection.Warning) as e:
            print(e)
            # Print custom error message
            if e.args[0] == 1644:
                flash(e.args[1])
            else:
                flash('There was an error posting to this page.')
    else:
        flash('There was an error posting to this page.')

    return redirect(request.referrer)

@mod.route('/groups/forms/remove_post', methods=['POST'])
@login_required
def remove_post_form():
    postID = request.form['postID']

    remove_post_form = RemovePostForm(request.form)
    if request.form and remove_post_form.validate_on_submit():
        # Only allow user who owns page to delete a post on that page
        post = post_model.Post.get_post_by_id(postID)
        page = page_model.Page.get_page_by_id(post.pageID)
        if page.pageType == page_model.Page.PAGE_TYPE_GROUP:
            if current_user.userID == post.authorID:
                page.remove_post(postID)
            else:
                abort(403)
    else:
        flash('There was an error removing this post.')

    return redirect(request.referrer)

@mod.route('/groups/forms/join_group', methods=['POST'])
@login_required
def join_group():
    groupID = request.form['groupID']
    userID = request.form['userID']

    join_unjoin_form = JoinUnjoinForm(request.form)
    if request.form and join_unjoin_form.validate_on_submit():
        group = group_model.Group.get_group_by_id(groupID)
        try:
            group.join_group(userID)
        except (mysql.connection.Error, mysql.connection.Warning) as e:
            print(e)
            # Print custom error message
            if e.args[0] == 1644:
                flash(e.args[1])
            else:
                flash('There was an error joining this group.')
    else:
        flash('There was an error joining this group.')

    return redirect(request.referrer)

@mod.route('/groups/forms/unjoin_group', methods=['POST'])
@login_required
def unjoin_group():
    groupID = request.form['groupID']
    userID = request.form['userID']

    join_unjoin_form = JoinUnjoinForm(request.form)
    if request.form and join_unjoin_form.validate_on_submit():
        group = group_model.Group.get_group_by_id(groupID)
        try:
            group.unjoin_group(userID)
        except (mysql.connection.Error, mysql.connection.Warning) as e:
            print(e)
            # Print custom error message
            if e.args[0] == 1644:
                flash(e.args[1])
            else:
                flash('There was an error unjoining this group.')
    else:
        flash('There was an error unjoining this group.')

    return redirect(request.referrer)

@mod.route('/likes/forms/like_unlike', methods=['POST'])
@login_required
def like_unlike():
    postID = request.json['postID']
    authorID = request.json['authorID']
    contentType = request.json['contentType']
    response = {'like_button':None, 'count':None}
    if contentType == 'po' or contentType == 'cm':
        cursor = mysql.connection.cursor()
        #check if like or unlike
        query = '''SELECT COUNT(*) AS count
                FROM Likes L 
                WHERE L.parentID = {0}
                AND L.authorID = {1}
                AND L.contentType = "{2}"
                '''.format(postID, authorID, contentType)    

        cursor.execute(query)

        result = cursor.fetchone()

        count = result['count']
        if count == 0:
            #like
            query = '''CALL `like`({0}, {1}, "{2}")
                    '''.format(postID, authorID, contentType)
            cursor.execute(query)
            mysql.connection.commit()
            response['like_button'] = 'unlike'
        else:
            #unlike
            query = '''CALL unlike({0}, {1}, "{2}")
                    '''.format(postID, authorID, contentType)
            cursor.execute(query)
            mysql.connection.commit()
            response['like_button'] = 'like'
        #get new like count
        query = '''SELECT COUNT(*) AS count
                FROM Likes L 
                WHERE L.parentID = {0}
                AND L.contentType = "{1}"
                '''.format(postID, contentType)  

        cursor.execute(query)

        result = cursor.fetchone()

        response['count'] = result['count']  
        return jsonify(response)
    else :
        return 'failure'
