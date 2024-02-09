from flask import Flask, jsonify, request
from flask_cors import CORS

from flask_jwt_extended import JWTManager, create_access_token, jwt_required
from itsdangerous import URLSafeTimedSerializer

from dotenv import load_dotenv
import os
import langchain as lc

from langchain_openai import ChatOpenAI
from langchain.schema import AIMessage, HumanMessage, SystemMessage

from langchain_core.prompts import ChatPromptTemplate

load_dotenv()


key = os.getenv("OPENAI_API_KEY")
from openai import OpenAI

client = OpenAI()

app = Flask(__name__)
CORS(app, origins=["http://localhost:5173"])

# TODO: LOGIN AND SIGNUP

system_msg = "You are an expert data analyst."
prompt = "Suggest some data analysis questions and ideas about the dataset for feature engineering. Do not write code."


# @app.route("/")
# def hello_world():
#     return "Hello, World!"


# def check_existing_user(username):
#     # Check if the username already exists in the file
#     with open("login_info.txt", "r") as f:
#         for line in f:
#             if username in line:
#                 return True
#     return False


# @app.route("/login", methods=["POST"])
# def login():


# @app.route("/signup", methods=["POST"])
# def signup():


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
    msgs_suggest_questions = [("system", system_msg), ("user", humanMessage)]
    chat = ChatOpenAI()

    chat.invoke(msgs_suggest_questions)
    rsrs_suggest_questions = chat(msgs_suggest_questions)
    return rsrs_suggest_questions.content


def truncate_string(s, max_length):
    if len(s) > max_length:
        return s[:max_length]
    else:
        return s


if __name__ == "__main__":
    app.run(debug=True)
