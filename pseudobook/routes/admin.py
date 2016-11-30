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
        return redirect(url_for('user_page.user_page', userID=current_user.userID))
    # Render login page
    elif request.method == 'GET':
        login_user_form = LoginUserForm()
        return render_template('login.html', form=login_user_form)
    # Validate login
    else:
        email = request.form['email']
        password = request.form['password']

        user = user_model.User.get_user_by_email(email)
        if user and user.verify_password(password):
            login_user(user)
            return redirect(url_for('user_page.user_page', userID=current_user.userID))
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

        firstName = request.form['firstName']
        lastName = request.form['lastName']
        email = request.form['email']
        password = request.form['password']
        password_B = request.form['password_B']

        create_user = CreateUserForm(request.form)
        if request.form and create_user.validate_on_submit():
            if user_model.User.get_user_by_email(email):
                flash('A user with that email already exists.')
                return redirect(url_for('admin.signup'))
            elif password != password_B:
                flash('The two passwords did not match.')
                return redirect(url_for('admin.signup'))
            else:
                new_user = user_model.User(None, firstName, lastName, email, user_model.User.hash_password(password))
                try:
                    new_user.userID = new_user.register_user()
                except (mysql.connection.Error, mysql.connection.Warning) as e:
                    print("Exeption of type {} occured: {}".format(type(e), e))
                else:
                    login_user(new_user)
                    return redirect(url_for('user_page.user_page', userID=new_user.userID))

        flash('There was an error in account creation. Please try again.')
        return redirect(url_for('admin.signup'))