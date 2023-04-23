# from flask_wtf import FlaskForm
# from wtforms import StringField, SubmitField
# from wtforms.validators import DataRequired, Email, Length


<<<<<<< HEAD
# class ContactForm(FlaskForm):
#     name = StringField('Name', validators=[DataRequired(), Length(max=255)])
#     email = StringField('Email', validators=[DataRequired(), Length(max=255), Email()])
#     message = StringField('Message',validators=[DataRequired(), Length(max=255)])
#     submitForm = SubmitField('Submit')
=======
class ContactForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(max=255)])
    email = StringField('Email', validators=[DataRequired(), Length(max=255), Email()])
    message = StringField('Message',validators=[DataRequired(), Length(max=255)])
    submitForm = SubmitField('Submit')

>>>>>>> 33638da92dffee8b4e12265a468d238001884063
