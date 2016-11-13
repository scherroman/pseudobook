from flask import Blueprint
from flask import render_template, url_for, request, redirect 
from flask_login import LoginManager, login_required, login_user, logout_user, current_user

from pseudobook.forms.login_user import LoginUser

'''
Login Manager
'''
login_manager_route = Blueprint('login_manager_route', __name__, template_folder='templates')
login_manager = LoginManager()
login_manager.login_view = 'login'

def initLoginManager(app):
    login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    user_obj = get_user_method(user_id)
    if user_obj:
        return user_obj
    return None

@login_manager_route.route('/login', methods=['GET', 'POST'])
def login():
    if not current_user.is_anonymous:
        return redirect(url_for('main_page'))
    if request.method == 'POST':
        if verify_password(request.form['username'], request.form['password']):
            login_user(get_user_by_name(request.form['username']))
            return redirect(url_for('user_view', username=current_user.username))
        else:
            # tell user about failed login
            flash('you failed to login')
            return redirect(url_for('login'))
    else:
        if not current_user.is_anonymous:
            return redirect(url_for('main_page'))
        login_user_form = LoginUser()
        return render_template('login.html', form=login_user_form)

@login_manager_route.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return redirect(request.referrer)

@login_manager_route.route('/signup', methods=['GET'])
def signup():
    create_user = CreateUser()
    return render_template('signup.html', form=create_user)

def verify_password(username_or_token, password):
    user = user_object.UserObject.verify_auth_token(username_or_token)
    if not user:
        user = user_object.UserObject.query.filter_by(username=username_or_token).first()
        if not user or not user.verify_password(password):
            return False
    g.user_object = user
    return True