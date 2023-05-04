#!/usr/bin/python
from flask import flash, render_template, request, redirect, session, url_for
from flask_login import login_required
from application import app, db
from application.models import User
from application.forms import RegisterForm, LoginForm, EditForm

from sqlalchemy.sql.functions import now

REGISTER_FORM_DATA = "register_form"
LOGGED_IN_USER = "user_id"


@app.route("/", methods=["GET", "POST"])
def index():
    current_user = get_current_user()
    return render_template("index.html", current_user=current_user)


def get_current_user():
    if LOGGED_IN_USER in session:
        user_id = session[LOGGED_IN_USER]
        return User.query.get(user_id)
    else:
        return None


@app.route("/login")
def login():
    login_form = LoginForm()
    current_user = get_current_user()
    return render_template(
        "/login.html", login_form=login_form, current_user=current_user
    )


@app.route("/login", methods=["GET", "POST"])
def validate_login():
    login_form = LoginForm()
    current_user = get_current_user()

    if login_form.validate_on_submit():
        user = User.query.filter_by(email=login_form.email.data).first()

        if user is not None and user.is_correct_password(login_form.password.data):
            session[LOGGED_IN_USER] = user.id
            user.last_login = now()
            db.session.commit()
            flash(f"{user.name} logged in successfully!")
            return redirect("/user")

        flash("Invalid email or password.")

    return render_template(
        "/login.html", login_form=login_form, current_user=current_user
    )


@app.route("/register", methods=["GET", "POST"])
def register():
    register_form = RegisterForm()

    if request.method == "POST" and register_form.validate():
        user = User.query.filter_by(email=register_form.email.data).first()
        if user:
            flash(f"{user.email } - Email already exists. Please log in.")
            return redirect("/login")

        new_user = User(
            name=register_form.name.data,
            email=register_form.email.data,
            address=register_form.address.data,
            phone=register_form.phone.data,
            club=register_form.club.data,
            password=register_form.password.data,
        )

        db.session.add(new_user)
        db.session.commit()

        flash(f"{new_user.name} successfully registered.")
        session[REGISTER_FORM_DATA] = request.form
        session[LOGGED_IN_USER] = new_user.id
        return redirect("/user")

    return render_template("register.html", register_form=register_form)


@app.route("/logout")
def logout():
    session.pop(LOGGED_IN_USER)
    flash(f"Logged out successfully!")
    return redirect("/")


@app.route("/tennis")
def tennis():
    current_user = get_current_user()
    return render_template("tennis.html", current_user=current_user)


@app.route("/user")
def user():
    current_user = get_current_user()

    if not current_user:
        flash("Please login.")
        return redirect("/login")

    user = User.query.filter_by(id=session.get(LOGGED_IN_USER)).first()

    return render_template(
        "user.html",
        email=user.email if user else None,
        username=user.name if user else None,
        address=user.address if user else None,
        phone=user.phone if user else None,
        club=user.club if user else None,
        current_user=current_user,
    )


@app.route("/user/edit", methods=["GET", "POST"])
def edit_user():
    current_user = get_current_user()
    if not current_user:
        flash("Please login.")
        return redirect("/login")

    user = User.query.filter_by(id=session.get(LOGGED_IN_USER)).first()
    form = EditForm(obj=user)  # Create form instance and populate with user data
    if form.validate_on_submit():
        form.populate_obj(user)  # Update user object with form data
        db.session.commit()
        flash("User updated successfully.")
        return redirect("/user")

    # Populate form fields with current user data
    form.name.data = current_user.name
    form.email.data = current_user.email
    form.address.data = current_user.address
    form.phone.data = current_user.phone
    form.club.data = current_user.club

    # Get the previous user information
    prev_user = {
        "name": user.name,
        "email": user.email,
        "address": user.address,
        "phone": user.phone,
        "club": user.club,
    }

    return render_template(
        "edit_user.html",
        form=form,
        current_user=current_user,
        prev_user=prev_user,
    )


@app.route("/delete_account", methods=["POST"])
@login_required
def delete_account():
    user = get_current_user()
    db.session.delete(user)
    db.session.commit()
    flash("Your account has been deleted.", "success")
    return redirect("index")
