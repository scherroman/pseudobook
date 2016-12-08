from flask_wtf import Form
from wtforms.fields import StringField, SubmitField
from wtforms.validators import DataRequired

class JoinUnjoinGroup(Form):
    userID = StringField('userID', validators=[DataRequired()])
    groupID = StringField('groupID', validators=[DataRequired()])

'''
author @roman
'''