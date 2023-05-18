#!/usr/bin/python
from application import bcrypt, db
from sqlalchemy.ext.hybrid import hybrid_property


class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    address = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(255), nullable=False)
    club = db.Column(db.String(255), nullable=False)
    _password = db.Column(db.String(100), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(
        db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now()
    )
    event = db.relationship("Event", secondary="userevent", backref="users")

    @hybrid_property
    def password(self):
        return self._password

    @password.setter
    def password(self, plaintext):
        self._password = bcrypt.generate_password_hash(plaintext).decode("utf-8")

    def is_correct_password(self, plaintext):
        return bcrypt.check_password_hash(self._password, plaintext)


class Event(db.Model):
    __tablename__ = "event"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=True)
    start_date = db.Column(db.Date, nullable=True)
    end_date = db.Column(db.Date, nullable=True)
    description = db.Column(db.Text, nullable=True)
    registrations = db.relationship("UserEvent", backref="event")

    def is_registered(self, user):
        return any(reg.user == user for reg in self.registrations)

    def register_user(self, user):
        if not self.is_registered(user):
            registration = UserEvent(user=user, event=self)
            db.session.add(registration)


class UserEvent(db.Model):
    __tablename__ = "userevent"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    event_id = db.Column(db.Integer, db.ForeignKey("event.id"))

    user = db.relationship("User", backref="registrations")
