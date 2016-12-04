from flask_wtf import Form
from wtforms.fields import StringField, SubmitField
from wtforms.validators import DataRequired

class RemovePost(Form):
    postID = StringField('postID', validators=[DataRequired()])

'''
author @roman
'''