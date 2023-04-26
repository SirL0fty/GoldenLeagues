#!/usr/bin/python
from flask import flash, render_template, request, redirect, abort, session
from application import app, db
from application.models import User
from werkzeug.datastructures import MultiDict
from application.forms import RegisterForm
from sqlalchemy.sql.functions import now

REGISTER_FORM_DATA = "register_form"
LOGGED_IN_USER = 'user_id'

@app.route('/', methods=['GET', 'POST'])
def index():

        return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    register_form = RegisterForm()

    if request.method == 'POST' and register_form.validate():
        user = User.query.filter_by(email=register_form.email.data).first()
        if user:
            flash(f"{user.email } - Email already exists. Please log in.")
            return redirect('/login')
        
        new_user = User(
            name=register_form.name.data,
            email=register_form.email.data,
            password=register_form.password.data
        )

        db.session.add(new_user)
        db.session.commit()
        
        flash(f"{new_user.name} successfully registered.")
        session[REGISTER_FORM_DATA] = request.form
        return redirect('/user')

    return render_template('register.html', form=register_form)


@app.route('/tennis')
def tennis():
        return render_template('tennis.html')

@app.route('/user')
def user():
        
        
        #add check for the session
        
        return render_template('user.html')