#!/usr/bin/python

from application import db, app
from application.models import User

USERS = [
    User(
        name="Mike",
        email="mikecrane@me.com",
        password="password123",
        address="Address1, Address2, City, County, PO167JU",
        phone="",
        club="Fareham Tennis Club",
    ),
    User(
        name="Sam",
        email="samuelaaronparker@gmail.com",
        password="password123",
        address="",
        phone="",
        club="",
    ),
    User(
        name="Kat",
        email="katrinadematos3@gmail.com",
        password="password123",
        address="",
        phone="",
        club="",
    ),
]

with app.app_context():
    db.session.add_all(USERS)
db.session.commit()

print("Database seeded successfully!")
