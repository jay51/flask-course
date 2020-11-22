from flask import Blueprint, render_template, request, redirect, url_for
from wtforms import Form, StringField, validators
from .modles import User, Conference, Team

main = Blueprint("main", __name__)
# Form stuff
class ConferenceForm(Form):
    name            = StringField("name", [validators.Length(min=4, max=25)])
    short_name      = StringField("short_name", [validators.Length(min=4, max=25)])
    abbreviation    = StringField("abbreviation", [validators.Length(min=2, max=25)])

@main.route("/")
def index():
    conferences = Conference.query.all()
    return render_template("index.html", conferences=conferences)

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
    if team_id is not None:
        team = Team.query.filter_by(id=team_id).first()
        return render_template("teams.html", team=team)

    teams = Team.query.all()
    return render_template("teams.html", teams=teams)


@main.route("/register/team", methods=["GET", "POST"])
def register_team():
    errors = []
    if request.method == "POST":
        for key, value in request.form.to_dict().items():
            if not value or len(value) < 2 and key != "conference_id":
                errors.mainend("{value} is not valid value for {key}".format(key=key.upper(), value=value))

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


@main.route("/about")
def about():
    return render_template("about.html")

