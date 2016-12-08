from flask_wtf import Form
from wtforms.fields import TextAreaField, StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Length

class CreateGroup(Form):
    groupName = StringField('groupName', validators=[DataRequired()], render_kw={"placeholder": "Group Name"})
    # groupType = StringField('groupType', validators=[DataRequired(), Length(max=2)], render_kw={"placeholder": "2-character Group Type"})

'''
author @edgar
'''