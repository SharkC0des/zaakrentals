from flask import Flask, render_template,redirect,request, session, url_for, flash
import logging
from flask_session import Session
from objects import Car, Booking, User
from datetime import datetime
from database import db
from functools import wraps

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

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash("Please log in to access this page", "warning")
            return redirect(url_for('login', next=request.url))
        
        user = User.query.get(session['user_id'])
        if not user or not user.is_admin:
            flash("Admin access required", "error")
            return redirect("/")
        
        return f(*args, **kwargs)
    return decorated_function


@app.route("/admin")
@admin_required
def admin_dashboard():
    cars = Car.query.all()
    users = User.query.all()
    bookings = Booking.query.all()
    return render_template("adminDashboard.html", 
                         cars=cars, 
                         users=users, 
                         bookings=bookings)

@app.route("/admin/delete-car/<int:car_id>", methods=["POST"])
@admin_required
def admin_delete_car(car_id):
    try:
        car = Car.query.get_or_404(car_id)
        car_model = car.model  # Store for flash message
        
        # Check if there are any active bookings for this car
        active_bookings = Booking.query.filter_by(car_id=car_id).count()
        
        if active_bookings > 0:
            flash(f"Cannot delete {car_model} - it has {active_bookings} active booking(s)", "error")
            return redirect(url_for('admin_dashboard'))
        
        db.session.delete(car)
        db.session.commit()
        
        flash(f"Successfully deleted {car_model}", "success")
        return redirect(url_for('admin_dashboard'))
        
    except Exception as e:
        db.session.rollback()
        flash(f"Error deleting car: {str(e)}", "error")
        return redirect(url_for('admin_dashboard'))

@app.route("/admin/clear-booking", methods=["GET", "POST"])
@admin_required
def admin_clear_booking():
    try:
        # Delete all bookings from the table
        Booking.query.delete()
        db.session.commit()
        flash("All bookings cleared successfully!", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"Error clearing bookings: {str(e)}", "error")
    
    return redirect("/admin")


@app.route("/admin/add-car", methods=["GET", "POST"])
@admin_required
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
        location = request.form.get("location")

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
                doors=int(doors),
                location=location
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
        # Debug: Print all form data
        print("\n=== FORM DATA RECEIVED ===")
        print(f"All form data: {request.form}")
        print(f"All form keys: {list(request.form.keys())}")
        print("=" * 50)
        
        location = request.form.get('location_name')
        start_date = request.form.get('start_date')
        end_date = request.form.get('end_date')
        
        # Debug: Print what we extracted
        print(f"location: '{location}'")
        print(f"start_date: '{start_date}'")
        print(f"end_date: '{end_date}'")
        
        # Store the rental dates in session for later use (only if they exist)
        session['rental_dates'] = {
            'start_date': start_date if start_date else None,
            'end_date': end_date if end_date else None
        }

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
        
        # Filter out cars that are already booked during the requested period
        if start_date and end_date:
            try:
                start_datetime = datetime.strptime(start_date, "%Y-%m-%d")
                end_datetime = datetime.strptime(end_date, "%Y-%m-%d")
                
                # Get all car IDs that are booked during this period
                booked_car_ids = db.session.query(Booking.car_id).filter(
                    Booking.start_date <= end_datetime,
                    Booking.end_date >= start_datetime
                ).all()
                
                # Extract just the IDs from the result
                booked_car_ids = [car_id[0] for car_id in booked_car_ids]
                
                # Filter out booked cars
                validCars = [car for car in validCars if car.id not in booked_car_ids]
                
                print(f"\nBooking Filter Applied:")
                print(f"  Date range: {start_date} to {end_date}")
                print(f"  Booked car IDs: {booked_car_ids}")
                print(f"  Available cars: {len(validCars)}")
            except ValueError as e:
                print(f"Error parsing dates: {e}")
        
        print(f"{'='*50}\n")
        
        return render_template('carPage.html', cars=validCars)
    
    return render_template("home.html", name=session.get("name"))


@app.route("/pay")
def pay():
    if 'selected_car_id' not in session:
        flash("Please select a car first", "error")
        return redirect(url_for('car_page'))
    
    car = Car.query.get_or_404(session['selected_car_id'])
    rental_dates = session.get('rental_dates', {})

    user_data = None
    if 'user_id' in session:
        user = User.query.get(session['user_id'])
        if user:
            user_data = {
                'name': user.name,
                'email': user.email
            }

    return render_template("pay.html", car=car, rental_dates=rental_dates, user_data=user_data)


@app.route("/select-car/<int:car_id>")
def select_car(car_id):
    car = Car.query.get_or_404(car_id)
    session['selected_car_id'] = car_id
    session['selected_car'] = {
        'model': car.model,
        'price': car.price,
        'image': car.image,
        'details': car.details,
        'vehicle_type': car.vehicle_type,
        'passengers': car.passengers,
        'doors': car.doors
    }
    return redirect(url_for('pay'))

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

    return redirect("/")

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

@app.route("/login", methods=["GET", "POST"])
def login():
    # Handle GET and POST requests
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        #throw error if user doesnt input either box
        if not email or not password:
            flash("Email and password are required to login", "error")
            return redirect("/")
        
        user = User.query.filter_by(email=email).first()

        if user and user.check_password(password):
            #this is a successful login yippee
            app.logger.info(f"Login successful for user: {email}")\
            
            #still figuring out what session does lol give me a min
            session['user_id'] = user.id
            session['name'] = user.name
            session['email'] = user.email
            session['is_admin'] = user.is_admin

            #bring admin to the admin dash
            if user.is_admin:
                flash(f"Welcom back Admin!", "success")
                return redirect("/admin")

            #send normies back to the home page
            else: 
                return redirect("/")

        else:
            #unsucessful
            flash("Invalid email or password", "error")
            app.logger.warning(f"Failed login attempt for email: {email}")
            return redirect("/")


    # If it's a GET request, render the login page
    return redirect("/")

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


