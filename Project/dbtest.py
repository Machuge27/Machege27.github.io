from flask import Flask
from app import db, Product

# Create a Flask application instance
app = Flask(__name__)

# Configure the Flask application instance (if necessary)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///products.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Bind the Flask application instance to the SQLAlchemy database instance
db.init_app(app)

# Create some sample products
sample_products = [
    Product(name='Apple', category='Fruits', price=1.99, old_price=None, image='img1.jpg'),
    Product(name='Banana', category='Fruits', price=0.99, old_price=None, image='img1.jpg'),
    Product(name='Potatoes', category='Fruits', price=0.99, old_price=None, image='img1.jpg'),
    Product(name='Oranges', category='Fruits', price=0.99, old_price=None, image='img1.jpg'),
    Product(name='Mangoes', category='Fruits', price=0.99, old_price=None, image='img1.jpg'),
    Product(name='Beans', category='Cereals', price=3.49, old_price=4.99, image='img1.jpg'),
    Product(name='Maize', category='Cereals', price=3.49, old_price=4.99, image='img1.jpg'),
    Product(name='Ndengu', category='Cereals', price=3.49, old_price=4.99, image='img1.jpg'),
    Product(name='Cereal A', category='Cereals', price=3.49, old_price=4.99, image='img1.jpg'),
    # Add more sample products as needed
]

# Use the application context
with app.app_context():
    # Add products to the database
    for product in sample_products:
        db.session.add(product)

    # Commit the changes
    db.session.commit()

    print("Sample data added successfully.")
