from flask import Flask, render_template, jsonify, request, url_for, redirect, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_migrate import Migrate
import json
import string
import random
import openai

# from chat import get_response

import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"

db = SQLAlchemy(app)
migrate = Migrate(app, db)


# Unique ID generator
def generate_id():
    characters = string.ascii_letters + string.digits
    id_num = "".join(random.choices(characters, k=8))
    # id_num = random.randint(10000000, 99999999)
    return id_num


class User(db.Model):
    id = db.Column(db.String(8), primary_key=True, default=generate_id)
    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)


# Load chats from the database
filename = "static/conversations.json"


# Load the existing database or initialize an empty one
def read_file(filename):
    while True:
        try:
            with open(filename, "r") as file:
                conversations = json.load(file)
            print("Database found.")
            # print(conversations)
        except FileNotFoundError:
            print("No existing database. Creating a new one.")
            conversations = []
        return conversations


def save_chats(conversations, filename):
    # Save the updated conversations to a JSON file
    with open(filename, "w") as file:
        json.dump(conversations, file, indent=4)
    print(f"Conversations saved to {filename}")


def getResponse(user_input):
    # Set up OpenAI API credentials
    openai.api_key = "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"

    # Send the user input to OpenAI
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": user_input},
        ],
    )

    # Get the response from OpenAI
    response_message = completion.choices[0].message["content"]

    # Return the response
    print("Response: ", response_message)
    return response_message


@app.route("/")
def home():
    if "email" in session:
        return render_template("home.html", email=session["email"])
    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        fullname = request.form["fullname"]
        email = request.form["email"]
        password = request.form["password"]
        hashed_password = generate_password_hash(password)
        new_user = User(full_name=fullname, email=email, password=hashed_password)
        print("Fullname: ", fullname)
        print("email: ", email)
        print("pass: ", password)

        db.session.add(new_user)
        db.session.commit()
        # Set emai in session
        session["email"] = email

        return redirect(url_for("home"))
    # return render_template("login.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        print("email: ", email)
        print("Password: ", password)
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            session["email"] = email
            return redirect(url_for("home"))
        return "Invalid email or password"
    return render_template("login.html")


@app.route("/logout")
def logout():
    session.pop("email", None)
    return redirect(url_for("home"))


@app.route("/conversations")
def get_conversations():
    while True:
        conversations = read_file(filename)
        return jsonify(conversations)


@app.route("/process", methods=["POST"])
def process_message():
    conversations = read_file(filename)

    # Get the user input from the request
    request_data = request.json
    conversation_id = request_data.get("chat_id")
    user_input = request_data.get("message")
    query = request.json.get("message")
    print("Message id: ", conversation_id)
    print("user input: ", user_input)
    print("request: ", request.json)
    # implement response logic
    response = getResponse(user_input)

    # Check if there's an ongoing conversation
    if conversation_id is None:
        # If there's no ongoing conversation, start a new one
        conversation_id = len(conversations) + 1
        # Create a new conversation dictionary
        conversation = {
            "conversation_id": conversation_id,
            "title": "New Conversation",
            "time-created": "2024-01-09",
            "last-opened": "2024-01-09",
            "highlight-status": False,
            "messages": [user_input],
            "responses": [response],
        }
        # Append the new conversation to the conversations list
        conversations.append(conversation)
        save_chats(conversations, filename)
        print("new data saved")

    else:
        print("Message id: ", conversation_id)
        # If there's an ongoing conversation, update the existing one
        C_conversation = next(
            (
                conv
                for conv in conversations
                if conv["conversation_id"] == conversation_id
            ),
            None,
        )
        if C_conversation:  # <= len(conversations):
            # Append the user input to the existing conversation
            # conversation = conversations[current_conversation_id - 1]
            C_conversation["messages"].append(user_input)
            # Here, you would process the user input and generate a response
            # For simplicity, we'll just echo back the user input as the response
            C_conversation["responses"].append(response)
            save_chats(conversations, filename)
            print("data saved saved to: ", C_conversation["title"])
        else:
            response = "Invalid conversation ID"

    # Return the response message
    return jsonify({"message": response})


@app.route("/delete-chats", methods=["POST"])
def delte_conversation():
    conversations = read_file(filename)
    request_data = request.json
    conversation_id = request_data.get("chatId")
    if conversation_id is not None:
        # If there's an ongoing conversation, update the existing one
        C_conversation = next(
            (
                conv
                for conv in conversations
                if conv["conversation_id"] == conversation_id
            ),
            None,
        )
        if C_conversation:
            conversations.remove(C_conversation)
            save_chats(conversations, filename)
            print(f"Conversation deleted [{conversation_id}]")
            return jsonify({"message": "Conversation deleted"})
    return jsonify({"message": "Invalid conversation ID"})


if __name__ == "__main__":
    app.static_folder = "static"
    db.create_all()
    app.run(debug=True)
