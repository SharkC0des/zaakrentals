#from flask import Flask, render_template, redirect, request, session
#from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from database import db

#db = SQLAlchemy()  # initialize without app yet

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///car_rental.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)  # bind SQLAlchemy to this app

    return app


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    #age = db.Column(db.Integer, nullable=False)
    password = db.Column(db.String(128), nullable=False)  # store hashed passwords
    is_admin = db.Column(db.Boolean, default=False)


    def set_password(self, password):
        from werkzeug.security import generate_password_hash
        self.password = generate_password_hash(password)
    
    def check_password(self, password):
        from werkzeug.security import check_password_hash
        return check_password_hash(self.password, password)
    
    def __repr__(self):
        return f'<User {self.name}>'




class Car(db.Model):
    __tablename__ = "cars"
    id = db.Column(db.Integer, primary_key=True)
    model = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    details = db.Column(db.String(255))
    image = db.Column(db.String(255))
    vehicle_type = db.Column(db.String(50))
    passengers = db.Column(db.Integer)
    doors = db.Column(db.Integer)
    location = db.Column(db.String(255))

    def __repr__(self):
        return f'<Car {self.make} {self.model}>'
    


class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    car_id = db.Column(db.Integer, db.ForeignKey("cars.id"))
    payment_status = db.Column(db.String(50))

    user = db.relationship("User", backref="bookings")
    car = db.relationship("Car", backref="bookings")

