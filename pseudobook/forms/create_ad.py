from flask_wtf import Form
from wtforms.fields import TextAreaField, StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired

class CreateAd(Form):
    itemName = TextAreaField('itemName', validators=[DataRequired()], render_kw={"placeholder": "Item Name"})
    company = TextAreaField('company', validators=[DataRequired()], render_kw={"placeholder": "Associated Company"})
    itemType = TextAreaField('itemType', validators=[DataRequired()], render_kw={"placeholder": "Item Type"})
    content = TextAreaField('content', validators=[DataRequired()], render_kw={"placeholder": "Item Description"})
    price = TextAreaField('price', validators=[DataRequired()], render_kw={"placeholder": "Item Price"})
    unitsAvailable = TextAreaField('unitsAvailable', validators=[DataRequired()], render_kw={"placeholder": "Units Available"})
    authorID = StringField('authorID', validators=[DataRequired()])