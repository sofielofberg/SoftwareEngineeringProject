from datetime import datetime

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

@app.route("/receipt/{id:int}")
@login_required
def receipt(receipt_id):
    # Could have methods: may_approve(receipt), may_handle(receipt), may_view(receipt)
    receipt = Receipt.get_by_id(receipt_id)
    if isinstance(current_user, Manager) and receipt.is_handled() and receipt.approved_by is None:
        return render_template("receiptViewApprove.html",
                           user=current_user, receipt=receipt)
    elif isinstance(current_user, Accountant) and receipt.is_unprocessed():
        return render_template("receiptViewHandle.html",
                           user=current_user, receipt=receipt)
    elif isinstance(current_user, Accountant):
        return render_template("receiptView.html",
                           user=current_user, receipt=receipt)
    elif isinstance(current_user, Salesman) and receipt.submitter == current_user:
        return render_template("receiptView.html",
                           user=current_user, receipt=receipt)
    else:
        return redirect(url_for("select"))

@app.route("/accountant")
@login_required
def accountant():
    receipt = Receipt(0,
                      "static/placeholderReceipt.png",
                      datetime.now(),
                      100.00,
                      124,
                      "eh")
    return render_template("receiptViewHandle.html",
                           user=current_user, receipt=receipt)

@app.route("/manager")
@login_required
def manager():
    receipt = Receipt(0,
                      "static/placeholderReceipt.png",
                      datetime.now(),
                      100.00,
                      124,
                      "eh")
    return render_template("receiptViewApprove.html",
                           user=current_user, receipt=receipt)

@app.route("/salesman")
@login_required
def salesman():
    receipt = Receipt(0,
                      "static/placeholderReceipt.png",
                      datetime.now(),
                      100.00,
                      124,
                      "eh")
    return render_template("receiptView.html",
                           user=current_user, receipt=receipt)
