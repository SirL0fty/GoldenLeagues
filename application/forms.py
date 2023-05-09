#!/usr/bin/python
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, FileField, TextAreaField
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


class EditForm(FlaskForm):
    name = StringField("Name", validators=[Optional(), Length(max=255)])
    email = StringField("Email", validators=[Optional(), Length(max=255), Email()])
    address = StringField("Address", validators=[Optional(), Length(max=255)])
    phone = StringField("Phone", validators=[Optional(), Length(max=255)])
    club = StringField("Club", validators=[Optional(), Length(max=255)])
    password = PasswordField("Current Password", validators=[Optional(), Length(min=6)])
    profile_picture = FileField("Profile Picture")
    submit = SubmitField("Save Changes")


class DeleteForm(FlaskForm):
    submit = SubmitField("Delete Account")


class NewsForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    content = TextAreaField("Content", validators=[DataRequired()])
    created_at = StringField("Created At", validators=[DataRequired()])
    image = FileField("Image", validators=[DataRequired()])
