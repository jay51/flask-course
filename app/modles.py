from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

from . import db

class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    username = db.Column(db.String(1000))
    role = db.Column(db.Integer, default=1) # role 0 is admin

    # get all the teams through a secondary table that stores id for a user and id for a team
    teams = db.relationship("Team", secondary="follows")

    def __repl__(self):
        return "<User {username}, {email}, {role}>".format(
            username=self.username,
            email=self.email,
            role=self.role,
        )

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)


class Conference(db.Model):
    __tablename__ = "conferences"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    short_name = db.Column(db.String, nullable=False)
    abbreviation = db.Column(db.String, nullable=False)
    # each conference will have many teams
    teams = db.relationship("Team")

    # The user who created this conference
    # user_creater = db.Column(db.Integer, db.ForeignKey("users.id"))

    def __repr__(self):
        return "<Conference {name}, {short_name}, {abbreviation}>".format(
            name=self.name,
            short_name=self.short_name,
            abbreviation=self.abbreviation,
        )


class Team(db.Model):
    __tablename__ = "teams"
    id                  = db.Column(db.Integer, primary_key=True)
    school              = db.Column(db.String, nullable=False)
    mascot              = db.Column(db.String, nullable=False)
    abbreviation        = db.Column(db.String, nullable=False)
    logos               = db.Column(db.String, nullable=False)
    create_date         = db.Column(db.DateTime, default=datetime.utcnow)
    # each team will have one conference, foreignkey to conference
    conference_id       = db.Column(db.Integer, db.ForeignKey("conferences.id"))

    # The user who created this team
    # user_creater = db.Column(db.Integer, db.ForeignKey("users.id"))

    # get all users part of this team through a secondary table that stores id for a user and id for a team
    users = db.relationship("User", secondary="follows")
    comments = db.relationship("Comment")


    def __repr__(self):
        return "<Team {school}, {mascot}, {abbreviation} {logos} {conference_id}>".format(
            school          = self.school,
            mascot          = self.mascot,
            abbreviation    = self.abbreviation,
            logos           = self.logos,
            conference_id   = self.conference_id,
        )


class Comment(db.Model):
    __tablename__ = "comments"
    id          = db.Column(db.Integer, primary_key=True)
    create_date = db.Column(db.DateTime, default=datetime.utcnow)
    user_id     = db.Column(db.Integer, db.ForeignKey("users.id"))
    # will query for you the user
    # will query for you the team
    user        = db.relationship("User")
    team_id     = db.Column(db.Integer, db.ForeignKey("teams.id"))
    team        = db.relationship("Team")
    comment     = db.Column(db.String, nullable=False)

    def __repl__(self):
        return "<Comment {user_id}, {team_id}, {comment}>".format(
            user_id=self.user_id,
            team_id=self.team_id,
            comment=self.comment,
        )


class Follow(db.Model):
    __tablename__ = "follows"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    team_id = db.Column(db.Integer, db.ForeignKey("teams.id"))

    def __repl__(self):
        return "<Follow {user_id}, {team_id}>".format(user_id=self.user_id, team_id=self.team_id)
