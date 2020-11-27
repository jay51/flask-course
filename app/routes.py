from flask import Blueprint, render_template, request, redirect, url_for
from wtforms import Form, StringField, validators
from flask_login import login_required, current_user

from .modles import User, Conference, Team, Comment, Follow
from . import db

main = Blueprint("main", __name__)

# Form stuff
class ConferenceForm(Form):
    name            = StringField("name", [validators.Length(min=4, max=25)])
    short_name      = StringField("short_name", [validators.Length(min=4, max=25)])
    abbreviation    = StringField("abbreviation", [validators.Length(min=2, max=25)])

@main.route("/")
def index():
    conferences = Conference.query.all()
    teams = Team.query.all()
    return render_template("index.html", conferences=conferences, teams=teams)

@main.route("/conferences")
def conferences():
    conference_id = request.args.get("conference_id", None)
    if conference_id is not None:
        conference = Conference.query.filter_by(id=conference_id).first()
        conference_name = conference.name if conference else None
        teams = conference.teams if conference else None
        return render_template("conferences.html", teams=teams, name=conference_name)

    conferences = Conference.query.all()
    return render_template("conferences.html", conferences=conferences)


@main.route("/register/conference", methods=["GET", "POST"])
def register_conference():
    form = ConferenceForm(request.form)
    if request.method == "POST" and form.validate():
        new_conf = Conference(
            name=form.name.data,
            short_name=form.short_name.data,
            abbreviation=form.abbreviation.data,
        )
        db.session.add(new_conf)
        db.session.commit()
        return redirect(url_for("conferences"))

    return render_template("register_conference.html", form=form)


@main.route("/teams")
def teams():
    team_id = request.args.get("team_id", None)
    print(current_user)
    if team_id is not None:
        team = Team.query.filter_by(id=team_id).first()
        comments = team.comments
        is_following = None
        if current_user.is_authenticated:
            is_following = Follow.query.filter_by(
                user_id=current_user.id,
                team_id=team_id,
            ).first() is not None

        return render_template("teams.html",
            team=team,
            comments=comments,
            is_following=is_following,
        )

    teams = Team.query.all()
    return render_template("teams.html", teams=teams)


@main.route("/register/team", methods=["GET", "POST"])
def register_team():
    errors = []
    if request.method == "POST":
        for key, value in request.form.to_dict().items():
            if not value or len(value) < 2 and key != "conference_id":
                errors.append("{value} is not valid value for {key}".format(key=key.upper(), value=value))

        if len(errors) == 0:
            new_team = Team(
                school          = request.form["school"],
                mascot          = request.form["mascot"],
                abbreviation    = request.form["abbreviation"],
                logos           = request.form["logo"],
                conference_id   = request.form["conference_id"],
            )
            # print(new_team)
            db.session.add(new_team)
            db.session.commit()
            return redirect(url_for("teams"))

    conferences = Conference.query.all()
    return render_template("register_team.html", conferences=conferences, errors=errors)

@main.route("/teams/comments/", methods=["POST"])
@login_required
def comments():
    if request.method == "POST":
        team_id = request.args.get("team_id", None)
        comment = request.form.get("comment", None)
        team = Team.query.filter_by(id=team_id).first()
        if not team_id or not team or not comment:
            flash("Somthing went wrong!")
            return redirect(url_for("main.teams"))


        new_comment = Comment(comment=comment)
        new_comment.user_id = current_user.id
        new_comment.team_id = team.id
        db.session.add(new_comment)
        db.session.commit()

        return redirect(url_for("main.teams", team_id=team_id))

