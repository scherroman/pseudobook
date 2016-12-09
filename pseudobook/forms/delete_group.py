from flask_wtf import Form
from wtforms.fields import StringField, SubmitField
from wtforms.validators import DataRequired

class DeleteGroup(Form):
    groupID = StringField('groupID', validators=[DataRequired()])
    userID = StringField('userID', validators=[DataRequired()])
'''
author @edgar
'''