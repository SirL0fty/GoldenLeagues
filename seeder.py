from application import app, db, User

USERS = [
    {name: 'Mike', email: 'mikecrane@me.com', password: 'password123'},
    {name: 'Sam', email: 'samuelaaronparker@gmail.com',
     password: 'password123'},
    {name: 'Kat', email: 'katrinadematos3@gmail.com',
     password: 'password123'},
]

with app.app_context():
    db.session.add_all(USERS)
    db.session.commit()

    user_models = dict(db.session.execute(db.select(User.name, User.id)).all())

print('Database seeded successfully!')
