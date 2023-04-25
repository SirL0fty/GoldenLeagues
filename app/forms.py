#!/usr/bin/python
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Email, Length

from app.database import db
from app.models import User, League

# class ContactForm(FlaskForm):
#     name = StringField('Name', validators=[DataRequired(), Length(max=255)])
#     email = StringField('Email', validators=[DataRequired(), Length(max=255), Email()])
#     message = StringField('Message',validators=[DataRequired(), Length(max=255)])
#     submitForm = SubmitField('Submit')

class UserForm(FlaskForm):
        name = StringField('Name', validators=[DataRequired(), Length(max=255)])
        email = StringField('Email', validators=[DataRequired(), Length(max=255), Email()])
        password = PasswordField('Password', validators=[DataRequired(), Length(max=255)])
        submit = SubmitField('Add User')
        
        
class LeagueForm(FlaskForm):
        name = StringField('Name', validators=[DataRequired(), Length(max=255)])
        owner_id = StringField('Owner', validators=[DataRequired(), Length(max=255)])
        submit = SubmitField('Add League')