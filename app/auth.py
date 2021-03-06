from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user

from .modles import User
from . import db

auth = Blueprint("auth", __name__)

@auth.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("profile.profile"))

    if request.method == "POST":
        email           = request.form.get("email")
        password        = request.form.get("password")
        remember        = True if request.form.get("remember") else False

        user = User.query.filter_by(email=email).first()
        if not user or not user.check_password(password):
            flash("Please check your login details and try again.!", "alert-warning")
            return redirect(url_for("auth.login"))

        login_user(user, remember=remember)
        flash('Logged in successfully.', "alert-success")
        next = request.args.get('next')

        if not is_safe_url(next):
            return abort(400)
        return redirect(url_for(next or "profile.profile"))

    return render_template("login.html")


@auth.route("/signup", methods=["GET", "POST"])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for("profile.profile"))

    if request.method == "POST":
        email           = request.form.get("email")
        password        = request.form.get("password")
        username        = request.form.get("username")
        # if there's a user with that email, send him to back to signup
        if User.query.filter_by(email=email).first():
            flash("Email address already exists!", "alert-warning")
            return redirect(url_for("auth.signup"))

        new_user = User( email=email, username=username)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        flash("User has been created seccusfly!", "alert-success")
        return redirect(url_for("auth.login"))

    return render_template("signup.html")


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    flash("User has been loged out!", "alert-success")
    return redirect(url_for("main.index"))

from urllib.parse import urlparse, urljoin

def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and \
           ref_url.netloc == test_url.netloc
