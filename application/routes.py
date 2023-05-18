#!/usr/bin/python
from flask import (
    flash,
    render_template,
    request,
    redirect,
    session,
    get_flashed_messages,
)
from application import app, db, csrf
from application.models import User, UserEvent, Event
from application.forms import (
    RegisterForm,
    LoginForm,
    EditForm,
    DeleteForm,
    NewsForm,
    EventForm,
)
from sqlalchemy.sql.functions import now
from datetime import datetime

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
    user_edit_form = EditForm(obj=user)  # Separate form variable for user edit
    event_form = EventForm()
    delete_form = DeleteForm()
    all_events = Event.query.all()

    users = User.query.all()

    for event in all_events:
        date_obj = datetime.strptime(str(event.start_date), "%Y-%m-%d")
        event.start_date = datetime.strftime(date_obj, "%d %B")

    return render_template(
        "admin.html",
        users=users,
        current_user=current_user,
        news_form=news_form,  # Use separate form variable for news form
        user_edit_form=user_edit_form,  # Pass user edit form to the template
        event_form=event_form,
        delete_form=delete_form,
        upcoming_events=all_events,
        username=current_user.name,
    )


@app.route("/login", methods=["GET", "POST"])
def login():
    login_form = LoginForm()
    current_user = get_current_user()

    if login_form.validate_on_submit():
        user = User.query.filter_by(email=login_form.email.data).first()

        if user is not None and user.is_correct_password(login_form.password.data):
            session[LOGGED_IN_USER] = user.id
            user.last_login = now()
            db.session.commit()
            flash(f"{user.name} logged in successfully!", "success")

            # check if user is an admin
            if user.is_admin:
                return redirect("/admin")
            else:
                return redirect("/user")

        else:
            flash("Invalid email or password.", "error")

    # Get flashed messages and pass them to the template
    messages = get_flashed_messages()

    return render_template(
        "/login.html",
        login_form=login_form,
        current_user=current_user,
        messages=messages,
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

    if current_user:
        userevent = UserEvent.query.filter_by(user_id=current_user.id).all()
    else:
        userevent = []

    all_events = Event.query.all()

    for event in all_events:
        date_obj = datetime.strptime(str(event.start_date), "%Y-%m-%d")
        event.start_date = datetime.strftime(date_obj, "%d %B")
        event.id = str(event.id)

    event_id = str(all_events[0].id) if all_events else None

    return render_template(
        "tennis.html",
        current_user=current_user,
        userevent=userevent,
        upcoming_events=all_events,
        event_id=event_id,
    )


@app.route("/user", methods=["GET", "POST"])
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
    userevent = UserEvent.query.filter_by(user_id=current_user.id).all()
    all_events = Event.query.all()

    for event in all_events:
        date_obj = datetime.strptime(str(event.start_date), "%Y-%m-%d")
        event.start_date = date_obj.strftime("%d %B")

    if not user:
        flash("Unable to retrieve user information.")
        return redirect("/login")

    if request.method == "POST":
        event_id = request.form.get("event_id")
        action = request.form.get("action")

        event = Event.query.get(event_id)
        if not event:
            flash("Event not found.")
            return redirect("/user")

        if action == "register_event":
            if event.is_registered(current_user):
                flash("You are already registered for this event.")
            else:
                event.register_user(current_user)
                db.session.commit()
                flash("Event registration successful.")
        elif action == "cancel_registration":
            if not event.is_registered(current_user):
                flash("You are not registered for this event.")
            else:
                user_event = UserEvent.query.filter_by(
                    event_id=event.id, user_id=current_user.id
                ).first()
                if user_event:
                    db.session.delete(user_event)
                    event.start_date = datetime.strptime(
                        str(event.start_date), "%Y-%m-%d"
                    ).date()  # Convert start_date back to datetime object
                    db.session.commit()
                    flash("Event registration canceled.")
                else:
                    flash("You are not registered for this event.")
        else:
            flash("Invalid action.")

        return redirect("/user")

    delete_form = DeleteForm()

    return render_template(
        "user.html",
        email=user.email,
        username=user.name,
        address=user.address,
        phone=user.phone,
        club=user.club,
        current_user=current_user,
        userevent=userevent,
        upcoming_events=all_events,
        delete_form=delete_form,
    )


@app.route("/user/edit", methods=["GET", "POST"])
def edit_user():
    current_user = get_current_user()
    if not current_user:
        flash("Please login.")
        return redirect("/login")

    user = User.query.filter_by(id=session.get(LOGGED_IN_USER)).first()
    form = EditForm(obj=user)
    userevent = UserEvent.query.filter_by(user_id=current_user.id).all()
    all_events = Event.query.all()

    if form.validate_on_submit():
        form.populate_obj(user)

        # Save the profile picture, if it was uploaded
        if form.profile_picture.data:
            user.profile_picture = form.profile_picture.data.read()

        db.session.commit()
        flash("User details have been updated.")
        return redirect("/user")

    # Populate form fields with current user data
    form.name.data = current_user.name
    form.email.data = current_user.email
    form.address.data = current_user.address
    form.phone.data = current_user.phone
    form.club.data = current_user.club

    delete_form = DeleteForm()

    if delete_form.validate_on_submit():
        # Handle delete user form submission
        db.session.delete(current_user)
        db.session.commit()
        flash("User account has been deleted.")
        return redirect("/login")

    # Get the previous user information
    prev_user = {
        "name": current_user.name,
        "email": current_user.email,
        "address": current_user.address,
        "phone": current_user.phone,
        "club": current_user.club,
    }

    return render_template(
        "edit_user.html",
        form=form,
        user=user,
        current_user=current_user,
        prev_user=prev_user,
        delete_form=delete_form,
        user_id=user.id,
        userevent=userevent,
        upcoming_events=all_events,
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

    if current_user.id == user_id:
        # User is deleting their own account
        db.session.delete(user)
        db.session.commit()
        flash("Your account has been deleted.")
        return redirect("/login")
    else:
        # Admin is deleting a user from the admin page
        db.session.delete(user)
        db.session.commit()
        flash("User account has been deleted.")
        return redirect("/admin")


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


@app.route("/create_event", methods=["GET", "POST"])
def create_event():
    current_user = get_current_user()
    if not current_user:
        flash("Please login.")
        return redirect("/login")
    if not current_user.is_admin:
        flash("You are not an admin.")
        return redirect("/")

    event_form = EventForm()
    delete_form = DeleteForm()

    if event_form.validate_on_submit():
        title = event_form.title.data
        description = event_form.description.data
        start_date = event_form.start_date.data
        end_date = event_form.end_date.data

        event = Event(
            title=title,
            description=description,
            start_date=start_date,
            end_date=end_date,
        )
        db.session.add(event)
        db.session.commit()

        flash("Event created successfully!")
        return redirect("/admin")

    elif delete_form.validate_on_submit():
        event_id = delete_form.id.data
        event = Event.query.get(event_id)
        if event:
            db.session.delete(event)
            db.session.commit()
            flash("Event deleted successfully!")
        else:
            flash("Event not found.")

        return redirect("/admin")

    return render_template(
        "create_event.html",
        current_user=current_user,
        event_form=event_form,
        delete_form=delete_form,
        upcoming_events=Event.query.all(),
    )


@app.route("/delete_event/<int:event_id>", methods=["POST"])
def delete_event(event_id):
    current_user = get_current_user()
    if not current_user:
        flash("Please login.")
        return redirect("/login")
    if not current_user.is_admin:
        flash("You are not an admin.")
        return redirect("/")

    event = Event.query.filter_by(id=event_id).first()
    if not event:
        flash("Event not found.")
        return redirect("/admin")

    delete_form = DeleteForm()
    delete_form.csrf_token.data = request.form.get("csrf_token")

    if delete_form.validate():
        db.session.delete(event)
        db.session.commit()
        flash("Event deleted successfully!")
    else:
        flash("Invalid CSRF token.")

    return redirect("/admin")


@app.route("/event")
def event():
    all_events = Event.query.all()

    return render_template("event.html", all_events=all_events)


@app.route("/register_event/<int:event_id>", methods=["GET", "POST", "DELETE"])
def register_event(event_id):
    current_user = get_current_user()
    if not current_user:
        flash("Please login.")
        return redirect("/login")

    event = Event.query.get(event_id)
    if not event:
        flash("Event not found.")
        return redirect("/")

    formatted_start_date = event.start_date.strftime("%d %B")

    if request.method == "POST":
        if event.is_registered(current_user):
            flash("You are already registered for this event.")
        else:
            event.register_user(current_user)
            registered_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            event.registered_at = registered_at
            db.session.commit()
            flash("Event registration successful.")
        return redirect("/user")

    elif request.method == "DELETE":
        if not event.is_registered(current_user):
            flash("You are not registered for this event.")
        else:
            user_event = UserEvent.query.filter_by(
                event_id=event.id, user_id=current_user.id
            ).first()
            db.session.delete(user_event)
            db.session.commit()
            flash("Event registration canceled.")
        return redirect("/user")

    else:
        return render_template(
            "tennis.html", event=event, formatted_start_date=formatted_start_date
        )
