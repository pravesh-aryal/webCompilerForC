from flask import Flask
from flask import render_template


app = Flask(__name__)


@app.route("/")
def home():
    return "HELLO WORLD THIS IS THE HOME PAGE"

@app.route("/hello")
def hello():
    return render_template("home.html")