from datetime import datetime

from flask import redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user

from main import app
from receipt import Receipt
from user import Accountant, Manager, Salesman, User


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
    return render_template(
        "receiptSelection.html", user=current_user, receipts=receipts
    )


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
def receipt(receipt_id: int):
    receipt = Receipt.get_by_id(receipt_id)
    if current_user.can_view(receipt):
        return render_template("receiptView.html", user=current_user, receipt=receipt)

    return redirect(url_for("select"))


@app.route("/handle/<int:receipt_id>", methods=["POST"])
@login_required
def handle(receipt_id: int):
    receipt = Receipt.get_by_id(receipt_id)
    if current_user.can_handle(receipt):
        current_user.handle(receipt)

    return redirect(url_for("receipt", receipt_id=receipt_id))


@app.route("/approve/<int:receipt_id>", methods=["POST"])
@login_required
def approve(receipt_id: int):
    receipt = Receipt.get_by_id(receipt_id)
    if current_user.can_approve(receipt):
        current_user.approve(receipt)

    return redirect(url_for("receipt", receipt_id=receipt_id))


@app.route("/deny/<int:receipt_id>", methods=["POST"])
@login_required
def deny(receipt_id: int):
    receipt = Receipt.get_by_id(receipt_id)
    if current_user.can_deny(receipt):
        current_user.deny(receipt)

    return redirect(url_for("receipt", receipt_id=receipt_id))


@app.route("/accountant")
@login_required
def accountant():
    receipt = Receipt(
        None, "/static/placeholderReceipt.png", 100.00, datetime.now(), 124
    )
    return render_template("receiptViewHandle.html", user=current_user, receipt=receipt)


@app.route("/manager")
@login_required
def manager():
    receipt = Receipt(
        None, "/static/placeholderReceipt.png", 100.00, datetime.now(), 124
    )
    return render_template(
        "receiptViewApprove.html", user=current_user, receipt=receipt
    )


@app.route("/salesman")
@login_required
def salesman():
    receipt = Receipt(
        None, "/static/placeholderReceipt.png", 100.00, datetime.now(), 124
    )
    return render_template("receiptView.html", user=current_user, receipt=receipt)
