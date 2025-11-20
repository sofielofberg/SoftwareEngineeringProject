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
        if user and user.password == password:
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

@app.route("/submit", methods=["GET", "POST"])
@login_required
def submit():
    if request.method == "POST" and isinstance(current_user, Salesman):
        amount = float(request.form.get("amount"))
        date = datetime.fromisoformat(request.form.get("date"))
        bank_stmt_id = int(request.form.get("bank_stmt_id"))
        receipt = Receipt(
            submitter=current_user,
            image_path="/static/placeholderReceipt.png",
            amount=amount,
            date=date,
            bank_stmt_id=bank_stmt_id,
        )
        receipt.save()
        return redirect(url_for("select"))

    return render_template("receiptSubmission.html", user=current_user)

@app.route("/receipt/<int:receipt_id>")
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
    receipt = Receipt(None,
                      "/static/placeholderReceipt.png",
                      datetime.now(),
                      100.00,
                      124)
    return render_template("receiptViewHandle.html",
                           user=current_user, receipt=receipt)

@app.route("/manager")
@login_required
def manager():
    receipt = Receipt(None,
                      "/static/placeholderReceipt.png",
                      datetime.now(),
                      100.00,
                      124)
    return render_template("receiptViewApprove.html",
                           user=current_user, receipt=receipt)

@app.route("/salesman")
@login_required
def salesman():
    receipt = Receipt(None,
                      "/static/placeholderReceipt.png",
                      datetime.now(),
                      100.00,
                      124)
    return render_template("receiptView.html",
                           user=current_user, receipt=receipt)
