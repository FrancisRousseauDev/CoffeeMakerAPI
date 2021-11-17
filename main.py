from flask import Flask
import os

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "<p>Application coffeeAPI loaded succesfully</p>"


@app.route("/consumptions")
def consumptions():
    user = os.getenv('credential.user', 'userX')
    return user
