from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user

from .modles import User, Follow, Team
from . import db

user_profile = Blueprint("profile", __name__)


@user_profile.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    # UPDATE USER INFO
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
            user.password   = user.set_password(password) if password else user.password

            db.session.commit()
            flash("Your Profile has been updated seccusfly!")

        return redirect(url_for("profile.profile"))

    return render_template("profile.html")


@user_profile.route("/user")
def show_user_profile():
    print(request.referrer)
    user_id = request.args.get("user_id", None)
    if user_id is not None:
        user = User.query.filter_by(id=user_id).first()
        if user is not None:
            return render_template("show_user_profile.html", user=user)

    return redirect(request.referrer or url_for("main.index"))


@user_profile.route("/user/follow", methods=["POST"])
@login_required
def user_follow():
    team_id = request.form.get("team_id", None)
    if team_id is not None:
        team = Team.query.filter_by(id=team_id).first()
        following = Follow.query.filter_by(
            team_id=team_id,
            user_id=current_user.id
        ).first()

        if team is not None and not following:
            new_follow = Follow(user_id=current_user.id, team_id=team.id)
            db.session.add(new_follow)
            flash("You started following {name}".format(name=team.mascot))
        else:
            # if user is already following then unfollow
            db.session.delete(following)

        db.session.commit()

    else:
        flash("Something Went wrong!")

    return redirect(request.referrer or url_for("main.index"))

