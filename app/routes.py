from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from . import db
from .models import User
from .forms import RegisterForm, LoginForm

auth_bp = Blueprint("auth", __name__)

@auth_bp.get("/")
def index():
    if current_user.is_authenticated:
        return redirect(url_for("auth.dashboard"))
    return redirect(url_for("auth.login"))

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("auth.dashboard"))

    form = RegisterForm()
    if form.validate_on_submit():
        email = form.email.data.lower().strip()

        if User.query.filter_by(email=email).first():
            flash("That email is already registered.", "warning")
            return redirect(url_for("auth.register"))

        user = User(email=email)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()

        flash("Account created. You can log in now.", "success")
        return redirect(url_for("auth.login"))

    return render_template("register.html", form=form)

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("auth.dashboard"))

    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data.lower().strip()
        user = User.query.filter_by(email=email).first()

        if not user or not user.is_active or not user.check_password(form.password.data):
            flash("Invalid credentials.", "danger")
            return redirect(url_for("auth.login"))

        login_user(user)
        next_url = request.args.get("next")
        return redirect(next_url or url_for("auth.dashboard"))

    return render_template("login.html", form=form)

@auth_bp.get("/logout")
@login_required
def logout():
    logout_user()
    flash("Logged out.", "info")
    return redirect(url_for("auth.login"))

@auth_bp.get("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html")

# Exchange:
from flask import send_from_directory
from flask import current_app, send_from_directory
import os

#@auth_bp.get("/exchange")
@auth_bp.route("/exchange", methods=["GET"], strict_slashes=False)
def exchange():
    carpeta = os.path.join(current_app.static_folder, "exchange")
    return send_from_directory(carpeta, "index.html")