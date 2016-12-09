from flask_wtf import Form
from wtforms.fields import TextAreaField, StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired

class EditPost(Form):
    content = TextAreaField('content', validators=[DataRequired()], render_kw={"placeholder": "Edit this post..."})
    postID = StringField('postID', validators=[DataRequired()])

'''
author @roman
'''