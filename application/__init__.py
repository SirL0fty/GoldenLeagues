#!/usr/bin/python
import os

from flask import Flask
from flask_bcrypt import Bcrypt
from dotenv import load_dotenv

from application.database import db

load_dotenv()

app = Flask(__name__)


@app.after_request
def add_vary_cookie(response):
    # Check if the response contains a permanent session cookie
    if "Set-Cookie" in response.headers and "session" in response.headers["Set-Cookie"]:
        # Add the "Vary: Cookie" header to the response
        response.headers["Vary"] = "Cookie"
    return response


db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
db_host = os.getenv("DB_HOST")
db_port = os.getenv("DB_PORT", "3306")
db_name = os.getenv("DB_NAME")

app.config[
    "SQLALCHEMY_DATABASE_URI"
] = f"mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"

app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
db.init_app(app)
bcrypt = Bcrypt(app)

from application import routes
