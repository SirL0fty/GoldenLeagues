#!/usr/bin/python
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Email, Length

class UserForm(FlaskForm):
        name = StringField('Name', validators=[DataRequired(), Length(max=255)])
        email = StringField('Email', validators=[DataRequired(), Length(max=255), Email()])
        password = PasswordField('Password', validators=[DataRequired(), Length(max=255)])
        submit = SubmitField('Add User')
        