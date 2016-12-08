from flask import Blueprint, flash
from flask import render_template, url_for, request, redirect 
from flask_login import login_required, current_user
from urllib.parse import urlparse, urljoin

from pseudobook.database import mysql

from pseudobook.models import group as group_model

from pseudobook.forms.create_group import CreateGroup as CreateGroupForm
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
    group_post_offset = int(user_post_offset) if user_post_offset else 0

    total_users = user_model.User.count_users(search)
    users = user_model.User.scroll_users(offset, USERS_PER_PAGE, search)
    prev_users = True if offset > 0 else False
    next_users = True if ((offset + 1) * USERS_PER_PAGE) < total_users else False

    # Scroll all posts made by user
    total_user_posts = page_model.Page.count_posts_for_page_type(page_model.Page.PAGE_TYPE_USER, None)
    user_posts = page_model.Page.scroll_posts_for_user_pages(user_post_offset, POSTS_PER_PAGE, None)
    prev_user_posts = True if user_post_offset > 0 else False
    next_user_posts = True if ((user_post_offset + 1) * POSTS_PER_PAGE) < total_user_posts else False



@mod.route('/groups/<string:groupID>', methods=['GET'])
@login_required
def group_page():
    pass

@mod.route('/groups/create', methods=['GET', 'POST'])
@login_required
def create():
    create_group_form = CreateGroupForm()
    return render_template('create.html', form=create_group_form)

@mod.route('/groups/forms/create', methods=['POST'])
def create_group_form():
    groupName = request.form['groupName']
    groupType = request.form['groupType']

    create_group_form = CreateGroupForm(request.form)

    if request.form and create_group_form.validate_on_submit():
        new_group = group_model.Group(None, groupName, groupType, current_user.userID)
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
