from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user
from .models import User
from . import db

auth = Blueprint("auth", __name__)

@auth.route("/login", methods=("GET", "POST"))
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        remember = True if request.form.get("remember") else False

        user = User.query.filter_by(email=email).first()

        # Check of user exists. If so, validate password via hash.
        if not user or not check_password_hash(user.password, password):
            flash("Invalid credentials!")
            return redirect(url_for("auth.login"))

        # User login successful, so redirect to profile page.
        login_user(user, remember=remember)
        return redirect(url_for("main.profile"))

    return render_template("login.html")

@auth.route("/signup", methods=("GET", "POST"))
def signup():
    if request.method == "POST":
        email = request.form.get("email")
        name = request.form.get("name")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()

        # If user is found, redirect to signup page with
        # message that account e-mail must be unique.
        if user:
            flash("E-mail address already in use!")
            return redirect(url_for("auth.signup"))

        # Create new user with form data and hash password.
        new_user = User(email=email, name=name, 
            password=generate_password_hash(password, method="scrypt"))
        # Persist the new user to database.
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for("auth.login"))

    return render_template("signup.html")

@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("main.index"))
