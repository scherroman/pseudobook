from flask_login import LoginManager

from pseudobook.database import mysql

from pseudobook.models import user

'''
Setup Login Manager
'''
login_manager = LoginManager()
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return user.get_userby_id(user_id)