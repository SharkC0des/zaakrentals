from flask import Flask, render_template,redirect,request, session, url_for
from flask_scss import Scss
from flask_sqlalchemy import SQLAlchemy
from objects import Car, Booking, User
from datetime import datetime

app = Flask(__name__)
Scss(app)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///car_rental.db'  # Use PostgreSQL later if needed
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
# End of sql alchemy import

app.config["SESSION_PERMANET"] = False
app.config["SESSOIN_TYPE"] = "filesystem"
SESSION(app) 
# "Home"

@app.route("/", methods=["POST", "GET"])
def index():
    return render_template("index.html", name=session.get("name"))

@app.route("/payment/<int:car_id>")
def payment(car_id):
    car = Car.query.get_or_404(car_id)
    return render_template("payment.html", car=car)

# Payment Portal
@app.route("/process_payment", methods=["POST"])
def process_payment():
    name = request.form["name"]
    email = request.form["email"]
    start_date = request.form["start_date"]
    end_date = request.form["end_date"]
    car_id = request.form["car_id"]

    # Create or get user
    user = User.query.filter_by(email=email).first()
    if not user:
        user = User(name=name, email=email)
        db.session.add(user)
        db.session.commit()

    # Create booking with date range
    booking = Booking(
         start_date=datetime.strptime(start_date, "%Y-%m-%d"),
        end_date=datetime.strptime(end_date, "%Y-%m-%d"),
        user_id=user.id,
        car_id=car_id,
        payment_status="Paid"
    )
    db.session.add(booking)
    db.session.commit()

    return redirect(url_for("home"))


def login():
    if request.method == "POST":
        session['name'] = request.form.get("name")


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        # Add example car if none exist
        if Car.query.count() == 0:
            example_car = Car(car_type="Sedan", image_url="/static/car.png")
            db.session.add(example_car)
            db.session.commit()
    app.run(debug=True)


