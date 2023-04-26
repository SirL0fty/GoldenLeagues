#!/usr/bin/python
from flask import flash, render_template, request, redirect, abort, session
from app import app
from app.models import User, db
from app.models import User
from werkzeug.datastructures import MultiDict
from app.forms import UserForm

USER_FORM_DATA = "user_form"

@app.route('/', methods=['GET', 'POST'])
def index():

        return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    user_form = UserForm()

    if request.method == 'POST' and user_form.validate():
        user = User.query.filter_by(email=user_form.email.data).first()
        if user:
            flash(f"{user.email } - Email already exists. Please log in.")
            return redirect('/login')
        
        new_user = User(
            name=user_form.name.data,
            email=user_form.email.data,
            password=user_form.password.data
        )

        db.session.add(new_user)
        db.session.commit()
        
        flash(f"{new_user.name} successfully registered.")
        return redirect('/user')

    return render_template('register.html', form=user_form)


@app.route('/tennis')
def tennis():
        return render_template('tennis.html')

@app.route('/user')
def user():
        
        
        #add check for the session
        
        return render_template('user.html')