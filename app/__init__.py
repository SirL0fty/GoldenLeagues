#!/usr/bin/python
import os

from flask import Flask
from dotenv import load_dotenv

from app.database import db
from app.models import *

load_dotenv()

app = Flask(__name__)

db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')
db_host = os.getenv('DB_HOST', '127.0.0.1')
db_port = os.getenv('DB_PORT', '3306')
db_name = os.getenv('DB_NAME')

app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
db.init_app(app)

from app import routes 
