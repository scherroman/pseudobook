from flask_login import LoginManager

from pseudobook.database import mysql

from pseudobook.models import user as user_model

'''
Setup Login Manager
'''
login_manager = LoginManager()
login_manager.login_view = 'admin.login'

@login_manager.user_loader
def load_user(user_id):
    return user_model.User.get_user_by_id(user_id)