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
