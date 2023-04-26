#!/usr/bin/python
from app import db

class User(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String(255), nullable=False)
        email = db.Column(db.String(255), unique=True, nullable=False)
        _password = db.Column(db.String(100), nullable=False)
        created_at = db.Column(db.DateTime, server_default=db.func.now())
        updated_at = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())
        
        # league = db.relationship('League', back_populates='owner')