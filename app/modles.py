from flask_login import UserMixin
from . import db

class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    username = db.Column(db.String(1000))
    role = db.Column(db.Integer, default=1)

    def __repl__(self):
        return "<User {username}, {email}, {role}>".format(
            username=self.username,
            email=self.email,
            role=self.role,
        )

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

