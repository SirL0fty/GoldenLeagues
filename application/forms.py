#!/usr/bin/python
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Email, Length, Optional


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


from wtforms.validators import Optional, Length, Email, ValidationError


class EditForm(FlaskForm):
    name = StringField("Name", validators=[Optional(), Length(max=255)])
    email = StringField("Email", validators=[Optional(), Length(max=255), Email()])
    address = StringField("Address", validators=[Optional(), Length(max=255)])
    phone = StringField("Phone", validators=[Optional(), Length(max=255)])
    club = StringField("Club", validators=[Optional(), Length(max=255)])
    password = PasswordField("Current Password", validators=[Optional(), Length(min=6)])
    submit = SubmitField("Save Changes")
