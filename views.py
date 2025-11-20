from flask import render_template, request, redirect, url_for
from flask_login import login_required, login_user, current_user, logout_user

from main import app
from receipt import Receipt
from accountant import Accountant
from manager import Manager
from salesman import Salesman
from user import User

@app.route("/")
def welcome():
    return render_template("welcome.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        user = User.get_by_username(username)
        if user.password == password:
            login_user(user)
            return redirect(url_for("select"))

    return render_template("login.html")

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("welcome"))

@app.route("/new_profile", methods=["GET", "POST"])
def new_profile():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        role = request.form.get("role")
        if role == "salesman":
            user = Salesman(username, password)
        elif role == "accountant":
            user = Accountant(username, password)
        elif role == "manager":
            user = Manager(username, password)

        user.save()

        return redirect(url_for("login"))

    return render_template("newProfile.html")

@app.route("/select")
@login_required
def select():
    receipts = Receipt.get_all()
    return render_template("receiptSelection.html",
                           user=current_user, receipts=receipts)

@app.route("/submit")
@login_required
def submit():
    return render_template("receiptSubmission.html")

@app.route("/accountant")
@login_required
def accountant():
    return render_template("receiptViewAccountant.html")

@app.route("/manager")
@login_required
def manager():
    return render_template("receiptViewManager.html")

@app.route("/salesman")
@login_required
def salesman():
    return render_template("receiptViewSalesman.html")
