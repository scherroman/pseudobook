from flask.ext.wtf import Form
from wtforms.fields import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired

class CreateUser(Form):
	firstName = StringField('firstName', validators=[DataRequired()], render_kw={"placeholder": "First Name"})
	lastName = StringField('lastName', validators=[DataRequired()], render_kw={"placeholder": "Last Name"})
	email = StringField('email', validators=[DataRequired()], render_kw={"placeholder": "Email"})
	password = PasswordField('password', validators=[DataRequired()], render_kw={"placeholder": "password"})

	address = StringField('address', render_kw={"placeholder": "Address"})
	city = StringField('city', render_kw={"placeholder": "City"})
	state = StringField('state', render_kw={"placeholder": "State"})
	zipCode = StringField('zipCode', render_kw={"placeholder": "Zip Code"})
	telephone = StringField('telephone', render_kw={"placeholder": "Telephone"})
    
'''
author @roman
'''