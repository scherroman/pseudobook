from flask_wtf import Form
from wtforms.fields import TextAreaField, StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired

class RemoveComment(Form):
    commentID = StringField('commentID', validators=[DataRequired()])

'''
author @roman
'''