from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Email, Length


class ContactForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(max=255)])
    email = StringField('Email', validators=[DataRequired(), Length(max=255), Email()])
    message = StringField('Message',validators=[DataRequired(), Length(max=255)])
    submitForm = SubmitField('Submit')