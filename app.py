from flask import Flask


app = Flask(__name__)


@app.route("/")
def home():
    return "HELLO WORLD THIS IS THE HOME PAGE"

@app.route("/hello")
def hello():
    return "This is hello page"