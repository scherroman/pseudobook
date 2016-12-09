from flask_wtf import Form
from wtforms.fields import StringField, TextField
from wtforms.validators import DataRequired

class CreateAd(Form):
    itemName = StringField('itemName', validators=[DataRequired()], render_kw={"placeholder": "Item Name"})
    company = StringField('company', validators=[DataRequired()], render_kw={"placeholder": "Associated Company"})
    itemType = StringField('itemType', validators=[DataRequired()], render_kw={"placeholder": "Item Type"})
    content = TextField('content', validators=[DataRequired()], render_kw={"placeholder": "Item Description"})
    price = StringField('price', validators=[DataRequired()], render_kw={"placeholder": "Item Price"})
    unitsAvailable = StringField('unitsAvailable', validators=[DataRequired()], render_kw={"placeholder": "Units Available"})
