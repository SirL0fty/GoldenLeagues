#!/usr/bin/python
from flask import flash, render_template, request, redirect, abort, session
from app import app, db
from app.models import User, League
from werkzeug.datastructures import MultiDict
from app.forms import UserForm
# from app.forms import ContactForm

USER_FORM_DATA = "user_form"

@app.route('/', methods=['GET', 'POST'])
def index():
    # form = ContactForm()

    # if request.method == 'POST' and form.validate():
    #     name = form.name.data
    #     email = form.email.data
    #     message = form.message.data

    #     # Do something with the data

    #     return render_template('index.html', form=form)

    # return render_template('index.html', form=form)
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
        user_form = UserForm()
        
        if user_form.validate():
                user = User()
                user.name = user_form.name.data
                user.email = user_form.email.data
                user.password = user_form.password.data
                
                db.session.add(user)
                try:
                        db.session.commit()
                except:
                        flash(f"{user.email } - Email already exists")
                return redirect('/user')
                
                flash(f'{user.name} successfully added')
                return redirect('/user')
        
        session[USER_FORM_DATA] = request.form
        return redirect('/user')

@app.route('/tennis')
def tennis():
        return render_template('tennis.html')

@app.route('/user')
def user():
        return render_template('user.html')
# @app.route('/home')
# def home():
#     return render_template ('home.html', title='home')