from flask_wtf import Form
from wtforms.fields import TextAreaField, StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired

class EditComment(Form):
    content = TextAreaField('content', validators=[DataRequired()], render_kw={"placeholder": "Edit this comment..."})
    commentID = StringField('commentID', validators=[DataRequired()])

'''
author @roman
'''