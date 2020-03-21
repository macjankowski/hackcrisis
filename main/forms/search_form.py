from flask_wtf import FlaskForm
from wtforms import StringField, TextField, SubmitField
from wtforms.validators import DataRequired, Length


class SearchForm(FlaskForm):
    """Contact form."""
    name = StringField('Search', [DataRequired()])

    # recaptcha = RecaptchaField()
    submit = SubmitField('Submit')