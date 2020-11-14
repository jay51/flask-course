#!/usr/bin/env python3
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
# from json import loads, dumps
from wtforms import Form, StringField, validators


DEVELOPMENT_ENV  = True
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://jay:pass@localhost:5432/itse2302"
app.config["SECRET_KEY"] = "HALO"
db = SQLAlchemy(app)


# DB stuff
class Conference(db.Model):
    __tablename__ = "conferences"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    short_name = db.Column(db.String, nullable=False)
    abbreviation = db.Column(db.String, nullable=False)
    # each conference will have many teams
    teams = db.relationship("Team")

    def __repr__(self):
        return "<Conference {name}, {short_name}, {abbreviation}>".format(
            name=self.name,
            short_name=self.short_name,
            abbreviation=self.abbreviation,
        )


class Team(db.Model):
    __tablename__ = "teams"
    id = db.Column(db.Integer, primary_key=True)
    school = db.Column(db.String, nullable=False)
    mascot = db.Column(db.String, nullable=False)
    abbreviation = db.Column(db.String, nullable=False)
    logos = db.Column(db.String, nullable=False)
    # each team will have one conference, foreignkey to conference
    conference_id = db.Column(db.Integer, db.ForeignKey("conferences.id"))

    def __repr__(self):
        return "<Team {school}, {mascot}, {abbreviation} {logos} {conference_id}>".format(
            school          = self.school,
            mascot          = self.mascot,
            abbreviation    = self.abbreviation,
            logos           = self.logos,
            conference_id   = self.conference_id,
        )


# Form stuff
class ConferenceForm(Form):
    name            = StringField("name", [validators.Length(min=4, max=25)])
    short_name      = StringField("short_name", [validators.Length(min=4, max=25)])
    abbreviation    = StringField("abbreviation", [validators.Length(min=2, max=25)])

# fuck this it's too tedious
"""
class teamForm(Form):
    school          = StringField("school", [validators.Length(min=4, max=25)])
    mascot          = StringField("mascot", [validators.Length(min=4, max=25)])
    abbreviation    = StringField("abbreviation", [validators.Length(min=2, max=25)])
    logos           = StringField("logos", [validators.Length(min=4, max=255)])
    # conference      = SelectField("Conference", choices=Conference.query.all())
"""

@app.route("/")
def index():
    conferences = Conference.query.all()
    return render_template("index.html", conferences=conferences)

@app.route("/conferences")
def conferences():
    conference_id = request.args.get("conference_id", None)
    if conference_id is not None:
        conference = Conference.query.filter_by(id=conference_id).first()
        conference_name = conference.name if conference else None
        teams = conference.teams if conference else None
        return render_template("conferences.html", teams=teams, name=conference_name)

    conferences = Conference.query.all()
    return render_template("conferences.html", conferences=conferences)


@app.route("/register/conference", methods=["GET", "POST"])
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


@app.route("/teams")
def teams():
    team_id = request.args.get("team_id", None)
    if team_id is not None:
        team = Team.query.filter_by(id=team_id).first()
        return render_template("teams.html", team=team)

    teams = Team.query.all()
    return render_template("teams.html", teams=teams)


@app.route("/register/team", methods=["GET", "POST"])
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


@app.route("/about")
def about():
    return render_template("about.html")


if __name__ == "__main__":
    app.run("0.0.0.0", 3000, debug=DEVELOPMENT_ENV)
