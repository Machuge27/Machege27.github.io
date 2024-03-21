import json

def add_employee(database):
    # Prompt user for employee details
    id = input("Enter the employee ID: ")
    name = input("Enter the employee name: ")
    position = input("Enter the employee position: ")

    # Create a new employee dictionary
    new_employee = {
        "id": id,
        "name": name,
        "position": position
    }

    # Append the new employee to the database
    database["employees"].append(new_employee)
    print("Employee added successfully!")


def save_database(database, filename):
    # Save the updated database to a JSON file
    with open(filename, 'w') as file:
        json.dump(database, file, indent=4)
    print(f"Database saved to {filename}")


def view_database(database):
    if len(database["employees"]) == 0:
        print("No employees in the database.")
    else:
        print("Employees:")
        for emp in database["employees"]:
            print(f"ID: {emp['id']}, Name: {emp['name']}, Position: {emp['position']}")

def main():
    filename = "database.json"

    # Load the existing database or initialize an empty one
    try:
        with open(filename, 'r') as file:
            database = json.load(file)
    except FileNotFoundError:
        database = {"employees": []}

    while True:
        print("\n1. Add Employee")
        print("2. View Database")
        print("3. Save Database")
        print("4. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            add_employee(database)
        elif choice == "2":
            view_database(database)
        elif choice == "3":
            save_database(database, filename)
        elif choice == "4":
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()