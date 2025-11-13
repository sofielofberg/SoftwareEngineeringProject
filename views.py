from flask import render_template, request

from main import app
from receipt import Receipt

@app.route("/")
def hello():
    return "Hello"

@app.route("/salesman", methods=("GET","POST"))
def salesman():
    if request.method == "POST":
        pass

    return render_template("receipt.html")
