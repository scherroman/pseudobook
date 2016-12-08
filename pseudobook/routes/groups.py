from flask import Blueprint, flash
from flask import render_template, url_for, request, redirect 
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
    search = request.values.get('search')
    offset = request.values.get('offset')
    offset = int(offset) if offset else 0
    group_post_offset = request.values.get('group_post_offset')
    group_post_offset = int(group_post_offset) if group_post_offset else 0

    total_groups = group_model.Group.count_groups(search)
    groups = group_model.Group.scroll_groups(offset, GROUPS_PER_PAGE, search)
    prev_groups = True if offset > 0 else False
    next_groups = True if ((offset + 1) * GROUPS_PER_PAGE) < total_groups else False

    # Scroll all posts made in groups
    total_group_posts = page_model.Page.count_posts_for_page_type(page_model.Page.PAGE_TYPE_GROUP, None)
    group_posts = page_model.Page.scroll_posts_for_group_pages(group_post_offset, POSTS_PER_PAGE, None)
    prev_group_posts = True if group_post_offset > 0 else False
    next_group_posts = True if ((group_post_offset + 1) * POSTS_PER_PAGE) < total_group_posts else False

    return render_template('groups.html', 
                            current_user=current_user, 
                            groups=groups, 
                            prev_groups=prev_groups, 
                            next_groups=next_groups,
                            offset=offset,
                            search=search,
                            group_posts=group_posts,
                            prev_group_posts=prev_group_posts,
                            next_group_posts=next_group_posts,
                            group_post_offset=group_post_offset)

@mod.route('/group/<string:groupID>', methods=['GET'])
@login_required
def group_page(groupID):
    posts_search = request.values.get('posts_search')
    posts_offset = request.values.get('posts_offset')
    posts_offset = int(posts_offset) if posts_offset else 0

    users_search = request.values.get('users_search')
    users_offset = request.values.get('users_offset')
    users_offset = int(users_offset) if users_offset else 0

    group = group_model.Group.get_group_by_id(groupID)
    if group:
        page = page_model.Page.get_page_by_group_id(groupID)

    total_posts = page.count_posts(posts_search)
    posts = page.scroll_posts(posts_offset, POSTS_PER_PAGE, posts_search)
    prev_posts = True if posts_offset > 0 else False
    next_posts = True if ((posts_offset + 1) * POSTS_PER_PAGE) < total_posts else False

    total_users = group.count_users(users_search)
    users = group.scroll_users(users_offset, USERS_PER_PAGE, users_search)
    prev_users = True if users_offset > 0 else False
    next_users = True if ((users_offset + 1) * USERS_PER_PAGE) < total_users else False

    make_post_form = MakePostForm()
    for post in posts:
        remove_post_form = RemovePostForm()
        post.remove_post_form = remove_post_form
    return render_template('group_page.html', 
                            current_user=current_user, 
                            group=group,
                            page=page,
                            posts=posts,
                            prev_posts=prev_posts, 
                            next_posts=next_posts,
                            posts_offset=posts_offset,
                            posts_search=posts_search,
                            users=users,
                            prev_users=prev_users,
                            next_users=next_users,
                            users_offset=users_offset,
                            users_search=users_search,
                            make_post_form=make_post_form)

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
            print(new_group.groupID)
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
            print(postID)
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

    # Only allow user who owns page to delete a post on that page
    post = post_model.Post.get_post_by_id(postID)
    page = page_model.Page.get_page_by_id(post.pageID)
    if page.pageType == page_model.Page.PAGE_TYPE_GROUP:
        if current_user.userID == post.authorID:
            page.remove_post(postID)
            print("here")
        else:
            abort(403)

    return redirect(request.referrer)
