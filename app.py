from flask import Flask, render_template,redirect,request, session, url_for, flash
import logging
from flask_session import Session
from objects import Car, Booking, User
from datetime import datetime
from database import db

app = Flask(__name__)


# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///car_rental.db'  # Use PostgreSQL later if needed
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'secret-key'

db.init_app(app)

#db = SQLAlchemy(app)
#i moved the db creation to database.py

# End of sql alchemy import

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app) 
# "Home"

# CARS DATABASE
@app.route("/cars")
def car_page():
    cars = Car.query.all()
    print(f"Found {len(cars)} cars")  # Debug line
    for car in cars:
        print(f"Car: {car.model}, Price: {car.price}")  # Debug line
    return render_template("carPage.html", cars=cars)


@app.route("/admin/add-car", methods=["GET", "POST"])
def admin_add_car():
    if request.method == "POST":
        # Get form data
        model = request.form.get("model")
        price = request.form.get("price")
        details = request.form.get("details")
        image = request.form.get("image")
        vehicle_type = request.form.get("vehicle_type")
        passengers = request.form.get("passengers")
        doors = request.form.get("doors")

        # Validate required fields
        if not all([model, price, image, vehicle_type, passengers, doors]):
            flash("Please fill in all required fields", "error")
            return render_template("addCar.html")

        try:
            # Create new car
            new_car = Car(
                model=model,
                price=int(price),
                details=details,
                image=image,
                vehicle_type=vehicle_type,
                passengers=int(passengers),
                doors=int(doors)
            )

            db.session.add(new_car)
            db.session.commit()

            flash(f"Successfully added {model} to inventory!", "success")
            return redirect(url_for("car_page"))

        except Exception as e:
            db.session.rollback()
            flash(f"Error adding car: {str(e)}", "error")
            return render_template("addCar.html")

    return render_template("addCar.html")


@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        location = request.form.get('location_name')
        start_date = request.form.get('start_date')
        start_time = request.form.get('start_time')
        end_date = request.form.get('end_date')
        end_time = request.form.get('end_time')

        # DETAILED DEBUG
        print(f"\n{'='*50}")
        print(f"SEARCH REQUEST:")
        print(f"  Location input: '{location}'")
        print(f"  Location type: {type(location)}")
        print(f"  Location length: {len(location) if location else 0}")
        print(f"{'='*50}")
        
        # Show all cars and their locations
        all_cars = Car.query.all()
        print(f"\nALL CARS IN DATABASE ({len(all_cars)}):")
        for car in all_cars:
            print(f"  - {car.model}: location='{car.location}'")
        
        # Perform the search
        if location and location.strip():
            validCars = Car.query.filter(Car.location.ilike(f'%{location}%')).all()
            print(f"\nSEARCH RESULTS:")
            print(f"  Query: Car.location.ilike('%{location}%')")
            print(f"  Found {len(validCars)} cars")
            for car in validCars:
                print(f"    ✓ {car.model} (location: {car.location})")
        else:
            validCars = Car.query.all()
            print(f"\nNo location specified, showing all {len(validCars)} cars")
        
        print(f"{'='*50}\n")
        
        return render_template('carPage.html', cars=validCars)
    
    return render_template("home.html", name=session.get("name"))


@app.route("/pay")
def pay():
    return render_template("pay.html")

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

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

@app.route("/login", methods=["GET", "POST"])
def login():
    # Handle GET and POST requests
    if request.method == "POST":
        name = request.form.get("name")
        password = request.form.get("password")  # You can add password validation logic here

        if name:  
            session['name'] = name
            app.logger.info(f"Login successful for user: {name}")

            # Check if 'next' is provided (the URL the user was trying to access before logging in)
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)  # Redirect to the original page
            else:
                return redirect("/")  # Default redirection to home page

        else:
            app.logger.warning("Login failed: Name not provided.")
            return "Login failed. Please try again.", 400

    # If it's a GET request, render the login page
    return render_template("/")  # Home page with login form

@app.route("/logout")
def logout():
    user_name = session.get('name', 'Unknown')  # Get the username for logging out
    session.clear()  # Clear the session to log the user out
    app.logger.info(f"User {user_name} logged out.")
    return redirect("/")

@app.route("/protected")
def protected():
    if 'name' not in session:
        # If user is not logged in, redirect to login page with a 'next' parameter
        return redirect(url_for('login', next=request.url))
    
    return "You are on a protected page!"  # Placeholder for a protected page


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        # Add example car if none exist
        # if Car.query.count() == 0:
        #     example_car = Car(car_type="Sedan", image_url="/static/car.png")
        #     db.session.add(example_car)
        #     db.session.commit()
    app.run(debug=True)


