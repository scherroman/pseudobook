from flask_wtf import Form
from wtforms.fields import TextAreaField, StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired

class MakeComment(Form):
    content = TextAreaField('content', validators=[DataRequired()], render_kw={"placeholder": "Respond to this post..."})
    postID = StringField('postID', validators=[DataRequired()])
    authorID = StringField('authorID', validators=[DataRequired()])

'''
author @roman
'''