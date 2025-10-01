from flask import Flask, render_template, redirect, request, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()  # initialize without app yet

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
    age = db.Column(db.Integer, nullable=False)
    password = db.Column(db.String(128), nullable=False)  # store hashed passwords
    bookings = db.relationship('Booking', backref='user', lazy=True)

    def __repr__(self):
        return f'<User {self.name}>'
    
    @classmethod
    def set_password(self, newPass: str):
        self.password = newPass

    def check_password(self, entry: str):
        if (self.password == entry):
            return True
        else:
            return False




class Car(db.Model):
    __tablename__ = 'cars'
    id = db.Column(db.Integer, primary_key=True)
    make = db.Column(db.String(50), nullable=False)
    model = db.Column(db.String(50), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    available = db.Column(db.Boolean, default=True)
    bookings = db.relationship('Booking', backref='car', lazy=True)

    def __repr__(self):
        return f'<Car {self.make} {self.model}>'
    
    @classmethod
    def set_available(self):
        self.available = True

    def set_unavailable(self):
        self.available = False

    def get_availability(self):
        return self.available


class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    car_id = db.Column(db.Integer, db.ForeignKey("car.id"))
    payment_status = db.Column(db.String(50))

    user = db.relationship("User", backref="bookings")
    car = db.relationship("Car", backref="bookings")

