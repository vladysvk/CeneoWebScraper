from wtforms import Form, StringField, SubmitField, validators

class ProductIdForm(Form):
    product_id = StringField("Product id", name='product_id', validators=[
        validators.DataRequired(message='Product id is required'),
        validators.Length(min=6, max=10,  message='Product id should have between 6 and 10 characters (inclusive)'),
        validators.Regexp(regex='^[0-9]*$', message='Product id can contain only digits')
    ])
    submit = SubmitField("Extract")