from app import app
from database import db
from objects import User

with app.app_context():
    db.create_all()

    if User.query.count() == 0:

        adam = User(
            name = "Adam Knell",
            email = "ajknell@syr.edu",
            is_admin = True,
        )
        adam.set_password("adamknell")

        zach = User(
            name = "Zach Grande",
            email = "zmgrande@syr.edu",
            is_admin = True,
        )
        zach.set_password("zachgrande")

        ado = User(
            name = "Ado Nyarko",
            email = "anyarko@syr.edu",
            is_admin = True,
        )
        ado.set_password("adonyarko")

        katie = User(
            name = "Katie Matulac",
            email = "kfmatula@syr.edu",
            is_admin = False,
        )
        katie.set_password("katiematulac")

        joe = User(
            name = "Joe Shmo",
            email = "joeshmo@syr.edu",
            is_admin = False,
        )
        joe.set_password("joeshmo")

        db.session.add_all([adam, ado, zach, katie, joe])
        db.session.commit()

    else:
        print(f"Database already has {User.query.count()} users. Skipping seed.")



