#!/usr/bin/python
from app.database import db


class User(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String(255))
        email = db.Column(db.String(255))
        password = db.Column(db.String(255))
        created_at = db.Column(db.DateTime, server_default=db.func.now())
        updated_at = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())
        
        league = db.relationship('League', back_populates='owner')
        

class League(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String(255))
        owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
        created_at = db.Column(db.DateTime, server_default=db.func.now())
        updated_at = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())

        user = db.relationship('User', back_populates='league')