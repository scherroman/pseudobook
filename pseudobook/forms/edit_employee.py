from flask_wtf import Form
from wtforms.fields import StringField
from wtforms.validators import DataRequired

class EditEmployee(Form):
    SSN = StringField('SSN', validators=[DataRequired()], render_kw={"placeholder": "New SSN"})
    hourlyRate = StringField('hourlyRate', validators=[DataRequired()], render_kw={"placeholder": "New Hourly Rate"})
    userID = StringField('userID', validators=[DataRequired()])