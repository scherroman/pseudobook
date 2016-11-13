from flask import Flask, render_template, url_for, jsonify, request, redirect 
from flask_mysqldb import MySQL

app = Flask(__name__)

'''
View Routing
'''
from pseudobook.routes import login_manager

login_manager.initLoginManager(app)
app.register_blueprint(login_manager.login_manager_route)

@app.route('/', methods=['GET'])
def main_page():
    return render_template('main.html', current_user=login_manager.current_user)

print(app.url_map)

'''
Run
'''
if __name__ == '__main__':
    app.run(debug=True)