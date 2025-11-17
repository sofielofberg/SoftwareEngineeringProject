from flask import render_template, request

from main import app
from receipt import Receipt

@app.route("/")
def welcome():
    return render_template("welcome.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/new_profile")
def new_profile():
    return render_template("newProfile.html")

@app.route("/select")
def select():
    receipts = Receipt.query.all()
    return render_template("receiptSelection.html", receipts=receipts)

@app.route("/submit")
def submit():
    return render_template("receiptSubmission.html")

@app.route("/accountant")
def accountant():
    return render_template("receiptViewAccountant.html")

@app.route("/manager")
def manager():
    return render_template("receiptViewManager.html")

@app.route("/salesman")
def salesman():
    return render_template("receiptViewSalesman.html")
