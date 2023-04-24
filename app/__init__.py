#!/usr/bin/python
from flask import Flask

app = Flask(__name__)
app.config['SECRET_KEY'] = 'sQ9kocDCG2kMAfrjsHAmBpxui3XkEa6ZQReTiqDd'

from app import routes 


# from dotenv import load_dotnev 

# load_dotnev()
# from email_validator import validate_email, EmailNotValidError
# def is_valid_email(email):
#     try:
#         valid = validate_email(email)
#         email = valid.email
#         except EmailNotValidError as e:
#         return False
#         return True
# if is_valid_email('test@example.com'):
#     print('Valid email!')
# else:
#     print('Invalid email.')


