#!/usr/bin/python
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Email, Length


class RegisterForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired(), Length(max=255)])
    email = StringField("Email", validators=[DataRequired(), Length(max=255), Email()])
    address = StringField("Address", validators=[DataRequired(), Length(max=255)])
    phone = StringField("Phone", validators=[DataRequired(), Length(max=255)])
    club = StringField("Club", validators=[DataRequired(), Length(max=255)])
    password = PasswordField("Password", validators=[DataRequired(), Length(max=255)])
    submit = SubmitField("Add User")


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Length(max=255), Email()])
    password = PasswordField("Password", validators=[DataRequired(), Length(max=255)])
    submit = SubmitField("Login")

class EditForm(FlaskForm)