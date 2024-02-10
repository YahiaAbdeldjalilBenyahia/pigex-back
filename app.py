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
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

key = os.getenv("OPENAI_API_KEY")
from openai import OpenAI

client = OpenAI()

app = Flask(__name__)
CORS(app, origins="http://localhost:5173")

# TODO: LOGIN AND SIGNUP
llm = ChatOpenAI(openai_api_key=key)

system_msg = "You are an expert data analyst."

prompt = ChatPromptTemplate.from_messages([("system", system_msg), ("user", "{input}")])

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


@app.route("/chainify", methods=["POST"])
def askgpt():
    req = request.json
    if not req:  # Check if data is present
        return jsonify({"error": "No data found in the request"}), 400
    data_description = req["dataDescription"]
    data = req["data"]
    humanMessage = truncate_string(
        f"{data_description}\n{data}\n Help me analyse this data. do not write code.",
        4097,
    )

    chain = prompt | llm
    output_parser = StrOutputParser()
    chain = prompt | llm | output_parser

    response = chain.invoke({"input": humanMessage})

    return response


def truncate_string(s, max_length):
    if len(s) > max_length:
        return s[:max_length]
    else:
        return s


if __name__ == "__main__":
    app.run(debug=True)
