#!/usr/bin/python

from application import db, app
from application.models import User

USERS = [
    
    User(
        name="Kat",
        email="katrinadematos3@gmail.com",
        _password="CoolCat",
        address="26 Starbuck Road",
        phone="07801506457",
        club="CoolDaddy",
    ),
]

with app.app_context():
    db.session.add_all(USERS)
db.session.commit()

print("Database seeded successfully!")
