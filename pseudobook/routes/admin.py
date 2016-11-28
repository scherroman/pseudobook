from flask import Blueprint, flash
from flask import render_template, url_for, request, redirect 
from flask_login import login_user, logout_user, login_required, current_user

from pseudobook.database import mysql

from pseudobook.models import user as user_model

from pseudobook.forms.login_user import LoginUser as LoginUserForm
from pseudobook.forms.create_user import CreateUser as CreateUserForm

'''
Setup Blueprint
'''
mod = Blueprint('admin', __name__, template_folder='../templates/admin')

'''
Routes
'''
@mod.route('/login', methods=['GET', 'POST'])
def login():
    # User already logged in
    if not current_user.is_anonymous:
        return redirect(url_for('user_page', userID=current_user.userID))
    # Render login page
    elif request.method == 'GET':
        login_user_form = LoginUserForm()
        return render_template('login.html', form=login_user_form)
    # Validate login
    else:
        if verify_password(request.form['email'], request.form['password']):
            login_user(get_user_by_email(request.form['email']))
            return redirect(url_for('user_page', userID=current_user.userID))
        else:
            # tell user about failed login
            flash('Invalid login credentials')
            return redirect(url_for('admin.login'))

@mod.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return redirect(request.referrer)

@mod.route('/signup', methods=['GET', 'POST'])
def signup():

    # Render signup page
    if request.method == 'GET':
        create_user_form = CreateUserForm()
        return render_template('signup.html', form=create_user_form)
    # Validate signup
    else:
        create_user = CreateUserForm(request.form)

        if request.form and create_user.validate_on_submit():
            if user_model.User.get_user_by_email(request.form['email']):
                flash('A user with that email already exists.')
                return redirect(url_for('admin.signup'))
            elif request.form['password'] != request.form['password_B']:
                flash('The two passwords did not match.')
                return redirect(url_for('admin.signup'))
            else:
                try:
                    created_user = user_model.User.register_user(request.form['firstName'], request.form['lastName'], request.form['email'], request.form['password_hash'])
                except (mysql.connection.Error, mysql.connection.Warning) as e:
                    print(e)
                else:
                    login_user(created_user)
                    return redirect(url_for('user_page', userID=created_user.userID))
                
        flash('There was an error in account creation. Please try again.')
        return redirect(url_for('admin.signup'))

'''
Helper Methods
'''
def verify_password(email, password):
    user = user_model.User.get_user_by_email(email)
    if user and user_model.verify_password(password):
        return True
    else:
        return False