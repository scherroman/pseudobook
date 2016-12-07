from flask_wtf import Form
from wtforms.fields import TextAreaField, StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired

class CreateGroup(Form):
    content = TextAreaField('groupName', validators=[DataRequired()], render_kw={"placeholder": "Group Name"})
    pageID = StringField('groupType', validators=[DataRequired()], render_kw={"placeholder": "Group Type"})
    authorID = StringField('ownerID', validators=[DataRequired()])

'''
author @edgar
'''