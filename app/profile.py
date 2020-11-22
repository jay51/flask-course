from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

from .modles import User
from . import db

user_profile = Blueprint("profile", __name__)


@user_profile.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    if request.method == "POST":
        user = User.query.filter_by(
            id=current_user.id,
            email=current_user.email,
            username=current_user.username,
        ).first()

        if not user:
            flash("Please check your login details and try again.!")
        else:
            email           = request.form.get("email")
            username        = request.form.get("username")
            password        = request.form.get("password")
            user.email      = email if email else user.email
            user.username   = username if username else user.username
            user.password   = generate_password_hash(password) if password else user.password

            db.session.commit()
            flash("Your Profile has been updated seccusfly!")

        return redirect(url_for("profile.profile"))

    return render_template("profile.html")

