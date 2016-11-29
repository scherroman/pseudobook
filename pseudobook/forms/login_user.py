from flask_wtf import Form
from wtforms.fields import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired

class LoginUser(Form):
    email = StringField('email', validators=[DataRequired()], render_kw={"placeholder": "Email"})
    password = PasswordField('password', validators=[DataRequired()], render_kw={"placeholder": "Password"})

'''
author @yvan
'''