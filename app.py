from flask import Flask
from flask import render_template
import subprocess



app = Flask(__name__)


@app.route("/")
def home():
    return "HELLO WORLD THIS IS THE HOME PAGE"

@app.route("/hello")
def hello():
    return render_template("home.html")

#executes when user runs the code
# @app.route("/run")
# def run():
#     #need to create a file with the text provided by the user
