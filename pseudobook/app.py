from flask import Flask, render_template
from flask_login import current_user

from pseudobook.database import mysql
from pseudobook.authentication import login_manager

# Blueprints
from pseudobook.routes import admin
from pseudobook.routes import users
<<<<<<< HEAD
from pseudobook.routes import manager

=======
from pseudobook.routes import groups
>>>>>>> group-creation/join/unjoin
'''
Setup
'''
app = Flask(__name__)
app.config['SECRET_KEY'] = '>\xee`o\xaeF\xa4|0Q\xc3*\xad\xac7:\n\xd6Yx\xd9;(\xdf'

# Initialize mysql & login_manager
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'pseudobook'
app.config['MYSQL_DB'] = 'pseudobook'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql.init_app(app)
login_manager.init_app(app)

'''
View Routing
'''
app.register_blueprint(admin.mod)
app.register_blueprint(users.mod)
<<<<<<< HEAD
app.register_blueprint(manager.mod)
=======
app.register_blueprint(groups.mod)
>>>>>>> group-creation/join/unjoin

@app.route('/', methods=['GET'])
def home_page():
	return render_template('main.html', current_user=current_user)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

# Prints helpful route map
print(app.url_map)

'''
Run
'''
if __name__ == '__main__':
    app.run(debug=True)