from flask import Flask, jsonify, request
from flask_cors import CORS
from dotenv import load_dotenv
import os
import langchain as lc
from langchain_community.chat_models import ChatOpenAI
from langchain.schema import AIMessage, HumanMessage, SystemMessage

load_dotenv()

key = os.getenv("OPENAI_API_KEY")
from openai import OpenAI

client = OpenAI()

app = Flask(__name__)
CORS(app, origins=["http://localhost:5173"])

system_msg = "You are an expert data analyst."
prompt = "Suggest some data analysis questions and ideas for feature engineering."


@app.route("/")
def hello_world():
    return "Hello, World!"


def check_existing_user(username):
    # Check if the username already exists in the file
    with open("login_info.txt", "r") as f:
        for line in f:
            if username in line:
                return True
    return False


@app.route("/login", methods=["POST"])
def login():
    # Extract login information from the request
    username = request.form.get("username")
    password = request.form.get("password")

    # Write login information to a file
    with open("login_info.txt", "a") as f:
        f.write(f"Username: {username}, Password: {password}\n")

    return jsonify({"message": "Login successful"}), 200


@app.route("/signup", methods=["POST"])
def signup():
    # Extract signup information from the request
    username = request.form.get("username")
    password = request.form.get("password")

    # Check if the username already exists
    if check_existing_user(username):
        return (
            jsonify(
                {
                    "message": "Username already exists. Please choose a different username."
                }
            ),
            400,
        )

    # Write signup information to the file
    with open("login_info.txt", "a") as f:
        f.write(f"Username: {username}, Password: {password}\n")

    return jsonify({"message": "Signup successful"}), 200


@app.route("/askgpt", methods=["GET", "POST"])
def askgpt():
    req = request.get_json()
    if not req:  # Check if data is present
        return jsonify({"error": "No data found in the request"}), 400
    data_description = req["dataDescription"]
    data = req["data"]
    humanMessage = truncate_string(f"{data_description}\n{data}\n{prompt}", 4097)
    msgs_suggest_questions = [
        SystemMessage(content=system_msg),
        HumanMessage(content=humanMessage),
    ]
    chat = ChatOpenAI()
    rsrs_suggest_questions = chat(msgs_suggest_questions)
    return rsrs_suggest_questions.content


def truncate_string(s, max_length):
    if len(s) > max_length:
        return s[:max_length]
    else:
        return s


if __name__ == "__main__":
    app.run(debug=True)
