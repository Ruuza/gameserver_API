from flask import url_for, redirect
from gameServer import app


@app.route("/")
def home():
    return "Hello World!"
