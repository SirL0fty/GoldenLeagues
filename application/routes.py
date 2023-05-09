#!/usr/bin/python
from flask import flash, render_template, request, redirect, session
from application import app, db
from application.models import User
from application.forms import RegisterForm, LoginForm, EditForm, DeleteForm, NewsForm
from sqlalchemy.sql.functions import now
import datetime

REGISTER_FORM_DATA = "register_form"
LOGGED_IN_USER = "user_id"


@app.route("/", methods=["GET", "POST"])
def index():
    current_user = get_current_user()
    print(current_user)
    return render_template("index.html", current_user=current_user)


def get_current_user():
    if LOGGED_IN_USER in session:
        user_id = session[LOGGED_IN_USER]
        return User.query.get(user_id)
    else:
        return None


@app.route("/admin", methods=["GET", "POST"])
def admin():
    current_user = get_current_user()
    if not current_user:
        flash("Please login.")
        return redirect("/login")
    if not current_user.is_admin:
        flash("You are not an admin.")
        return redirect("/login")

    news_form = NewsForm()
    users = User.query.all()
    return render_template(
        "admin.html", users=users, current_user=current_user, form=news_form
    )


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

            # check if user is an admin
            if user.is_admin:
                return redirect("/admin")
            else:
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

    logged_in_user_id = session.get(LOGGED_IN_USER)
    if not logged_in_user_id:
        flash("Unable to retrieve user information.")
        return redirect("/login")

    user = User.query.filter_by(id=logged_in_user_id).first()

    if not user:
        flash("Unable to retrieve user information.")
        return redirect("/login")

    return render_template(
        "user.html",
        email=user.email,
        username=user.name,
        address=user.address,
        phone=user.phone,
        club=user.club,
        current_user=current_user,
    )


@app.route("/user/edit", methods=["GET", "POST"])
def edit_user():
    current_user = get_current_user()
    if not current_user:
        flash("Please login.")
        return redirect("/login")

    user = User.query.filter_by(id=session.get(LOGGED_IN_USER)).first()
    print("user", user, user.id)
    form = EditForm(obj=user)

    if form.validate_on_submit():
        form.populate_obj(user)

        # Save the profile picture, if it was uploaded
        if form.profile_picture.data:
            user.profile_picture = form.profile_picture.data.read()

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
        "name": current_user.name,
        "email": current_user.email,
        "address": current_user.address,
        "phone": current_user.phone,
        "club": current_user.club,
    }

    delete_form = DeleteForm()
    print("rendering edit user form")

    return render_template(
        "edit_user.html",
        form=form,
        user=user,
        current_user=current_user,
        prev_user=prev_user,
        delete_form=delete_form,
        user_id=user.id,
    )


@app.route("/user/delete/<int:user_id>", methods=["POST"])
def delete_user(user_id):
    current_user = get_current_user()
    if not current_user:
        flash("Please login.")
        return redirect("/login")

    user = User.query.filter_by(id=user_id).first()
    if not user:
        flash("Unable to retrieve user information.")
        return redirect("/login")

    if current_user.id != user_id:
        flash("You can only delete your own account.")
        return redirect("/user/edit")

    db.session.delete(user)
    db.session.commit()
    print("user deleted")
    flash("User account has been deleted.")
    return redirect("/")


@app.route("/post_news", methods=["GET", "POST"])
def post_news():
    current_user = get_current_user()
    if not current_user:
        flash("Please login.")
        return redirect("/login")
    if not current_user.is_admin:
        flash("You are not an admin.")
        return redirect("/")

    form = NewsForm()

    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        created_at = datetime.now()
        image = form.image.data

        news_form = NewsForm(
            title=title, content=content, created_at=created_at, image=image
        )
        db.session.add(news_form)
        db.session.commit()

        flash("News post created successfully!")
        return redirect("/admin")

    return render_template(
        "post_news.html",
        form=form,
        current_user=current_user,
    )
