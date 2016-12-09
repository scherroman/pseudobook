from flask_wtf import Form
from wtforms.fields import StringField, SubmitField
from wtforms.validators import DataRequired

class LikeUnlike(Form):
    parentID = StringField('parentID', validators=[DataRequired()])
    authorID = StringField('authorID', validators=[DataRequired()])
    contentType = StringField('contentType', validators=[DataRequired()])

'''
author @roman
'''