from flask import Flask, render_template, jsonify, request
import json
import string
import random
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///products.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Unique ID generator
def generate_id():
    characters = string.ascii_letters + string.digits
    id_num = "".join(random.choices(characters, k=8))
    # id_num = random.randint(10000000, 99999999)
    return id_num

class Product(db.Model):
    id = db.Column(
        db.String(8), primary_key=True, default=generate_id
    )  # Using generate_id() as the default value
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Float, nullable=False)
    old_price = db.Column(db.Float, nullable=True)
    image = db.Column(db.String(200), nullable=True)

    def __repr__(self):
        return (
            f"Product(name={self.name}, category={self.category}, price={self.price})"
        )


@app.cli.command()
def init_db():
    db.create_all()
    print("Database initialized.")

@app.route("/")
def index():
    return render_template("roby.html")
    #return render_template("addProduct.html")

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f'<User {self.email}>'
    
@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    full_name = data.get('full_name')
    email = data.get('email')
    password = data.get('password')

    # Check if email is already registered
    if User.query.filter_by(email=email).first():
        return jsonify({'error': 'Email already registered'}), 400
    return render_template("register.html")

    # Create new user
    user = User(full_name=full_name, email=email, password=password)
    db.session.add(user)
    db.session.commit()

    return jsonify({'message': 'User registered successfully'}), 201    

@app.route("/api/products", methods=["GET"])
def get_products():
    products = Product.query.all()
    
    # Convert products to a list of dictionaries
    products_data = []
    for product in products:
        product_data = {
            "id": product.id,
            "name": product.name,
            "category": product.category,
            "price": product.price,
            "old_price": product.old_price,
            "image": product.image
        }
        products_data.append(product_data)
    #print(products_data)
    # Return JSON response
    return jsonify(products_data), 200


@app.route("/api/products", methods=["POST"])
def create_product():
    data = request.get_json()
    product = Products(**data)
    db.session.add(product)
    db.session.commit()
    return jsonify(product.__dict__), 201


if __name__ == "__main__":
    app.run(debug=True)
