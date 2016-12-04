from flask_wtf import Form
from wtforms.fields import TextAreaField, StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired

class MakePost(Form):
    content = TextAreaField('content', validators=[DataRequired()], render_kw={"placeholder": "What's on your mind?"})
    pageID = StringField('pageID', validators=[DataRequired()])
    authorID = StringField('authorID', validators=[DataRequired()])

'''
author @roman
'''