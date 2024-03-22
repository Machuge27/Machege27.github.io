from flask import Flask
from flask.cli import with_appcontext
from app import db, Product

# Create a Flask application instance
app = Flask(__name__)

# Configure the Flask application instance (if necessary)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///products.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Bind the Flask application instance to the SQLAlchemy database instance
db.init_app(app)

# Custom command to clear data
@app.cli.command("clear_data")
@with_appcontext
def clear_data():
    """
    Clear all data from the Product table.
    """
    # Use the application context
    with app.app_context():
        # Delete all rows from the Product table
        db.session.query(Product).delete()
        
        # Commit the changes
        db.session.commit()
        
        print("Data cleared successfully.")

        
"""
# Import necessary modules
from flask import Flask
from flask.cli import with_appcontext
from app import db, Product

# Create a Flask application instance
app = Flask(__name__)

# Configure the Flask application instance (if necessary)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///products.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Bind the Flask application instance to the SQLAlchemy database instance
db.init_app(app)

@app.cli.command("dbtest")
@with_appcontext
def dbtest():
    # Use the application context
    with app.app_context():
        # Perform some database test
        # For example, query the Product table and print the results
        products = Product.query.all()
        for product in products:
            print(product)

        print("Database test successful.")

# Register the custom command
if __name__ == '__main__':
    app.cli()  # This registers all the Flask CLI commands defined in the app
        
"""
