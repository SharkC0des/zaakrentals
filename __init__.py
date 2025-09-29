from flask import Flask, render_template,redirect,request, SESSION
from flask_scss import Scss
from flask_sqlalchemy import SQLAlchemy

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

def login():
    if request.method == "POST":
        session['name'] = request.form.get("name")


if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # creates tables
    print("Database initialized!")


