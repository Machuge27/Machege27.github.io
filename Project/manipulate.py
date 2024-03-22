from flask import Flask
from app import db, Product

# Create a Flask application instance
app = Flask(__name__)

# Configure the Flask application instance (if necessary)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///products.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Bind the Flask application instance to the SQLAlchemy database instance
db.init_app(app)

# Define functions to interact with the database
def clear_all_data():
    try:
        # Delete all rows from all tables
        db.session.query(Product).delete()
        # Commit the transaction
        db.session.commit()
        print("All data from the Product table has been cleared.")
    except Exception as e:
        db.session.rollback()
        print(f"An error occurred: {e}")

def add_data():
    name = input("Enter product name: ")
    category = input("Enter product category: ")
    price = float(input("Enter product price: "))
    old_price = float(input("Enter product old price (if any): ")) or None
    image = input("Enter product image filename: ")
    
    try:
        # Create a new product instance and add it to the database
        product = Product(name=name, category=category, price=price, old_price=old_price, image=image)
        db.session.add(product)
        db.session.commit()
        print("Product added successfully.")
    except Exception as e:
        db.session.rollback()
        print(f"An error occurred: {e}")

# Define the main function to interact with the user
def main():
    print("Welcome to the interactive program!")
    while True:
        print("\nOptions:")
        print("1. Clear all data")
        print("2. Add data")
        print("3. Exit")
        
        choice = input("Enter your choice (1/2/3): ")
        
        if choice == "1":
            clear_all_data()
        elif choice == "2":
            add_data()
        elif choice == "3":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")

if __name__ == "__main__":
    main()
