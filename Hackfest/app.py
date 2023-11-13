from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import secrets
import string
import random
import hashlib
from flask_migrate import Migrate
from flask_login import (
    LoginManager,
    UserMixin,
    login_user,
    login_required,
    logout_user,
    current_user,
)

app = Flask(__name__)
app.config["SECRET_KEY"] = secrets.token_hex(16)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db)"
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login_manager = LoginManager(app)
login_manager.login_view = "login"


def generate_id():
    characters = string.ascii_letters + string.digits
    id_num = "".join(random.choices(characters, k=8))
    # id_num = random.randint(10000000, 99999999)
    return id_num


class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.String(8), primary_key=True, default=generate_id)
    Firstname = db.Column(db.String(100), unique=True, nullable=False)
    Secondname = db.Column(db.String(100), unique=True, nullable=False)
    phone_number = db.Column(
        db.String(120), unique=True, nullable=False, name="phone_num"
    )
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)


# Routes
@app.route("/")
def index():
    return render_template("index.html")


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        # user = User.query.filter_by(username=username).first()

        if password == "1111" and username == "aaaa":
            # if user and check_password_hash(user.password, password):
            flash("Login successful", "success")
            return render_template("home.html")
        else:
            flash("Login failed. Check your username and password.", "danger")

    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        hashed_password = generate_password_hash(password, method="sha256")
        new_user = User(username=username, password=hashed_password)

        db.session.add(new_user)
        db.session.commit()

        print("Data received!!")
        flash("Account created successfully. You can now log in.", "success")
        return redirect(url_for("login"))

    return render_template("register.html")


@app.route("/home")
def home():
    return render_template("home.html")


@app.route("/chat")
def chat():
    def spec():
        try:
            with open("counties.json", "r") as file:
                specs = json.loads(file)
        except FileNotFoundError:
            print("Problem accessing location details.")

    return render_template("chat.html")


@app.route("/logout")
@login_required

def logout():
    logout_user()
    return redirect(url_for("login"))

counties_data = {
    'county1': {'sub_counties': [{'code': 'sub1', 'name': 'Sub 1'}, {'code': 'sub2', 'name': 'Sub 2'}]},
    'county2': {'sub_counties': [{'code': 'sub3', 'name': 'Sub 3'}, {'code': 'sub4', 'name': 'Sub 4'}]},
}

@app.route('/get_sub_counties/<county_code>')
def get_sub_counties(county_code):
    # Assuming you have data for sub-counties
    sub_counties = counties_data.get(county_code, {}).get('sub_counties', [])
    return jsonify({'sub_counties': sub_counties})

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)
