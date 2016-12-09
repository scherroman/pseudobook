from flask_wtf import Form
from wtforms.fields import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired

class RenameGroup(Form):
    groupID = StringField('groupID', validators=[DataRequired()])
    userID = StringField('userID', validators=[DataRequired()])
    content = TextAreaField('content', validators=[DataRequired()], render_kw={"placeholder": "New Group Name"})
'''
author @edgar
'''