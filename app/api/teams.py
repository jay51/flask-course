from flask import Blueprint, request, jsonify
from json import loads, dumps
from sqlalchemy import desc

from . import User, Conference, Team, Comment, Follow
from . import db

teams = Blueprint("teams", __name__, url_prefix="/api")

@teams.route("/teams")
def api_teams():
    teams = Team.query.order_by(desc(Team.create_date)).all()
    json = [
        {
            "id": team.id,
            "school": team.school,
            "mascot": team.mascot,
            "abbreviation": team.abbreviation,
            "logos": team.logos,
            "create_date": team.create_date,
            "users": [
                {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "Admin": user.role == 0
                } for user in  team.users
            ],
        } for team in teams
    ]
    return jsonify({"teams": json})

@teams.route("/teams/<team_id>")
def api_single_team(team_id):
    team = Team.query.filter_by(id=team_id).first()
    json = {
        "id": team.id, "school": team.school,
        "mascot": team.mascot,
        "abbreviation": team.abbreviation,
        "logos": team.logos,
        "create_date": team.create_date,
        "users": [
            {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "Admin": user.role == 0
            } for user in  team.users
        ],
    }
    return jsonify({"team": json})

@teams.route("/comments/teams/<team_id>")
def api_team_comments(team_id):
    team = Team.query.filter_by(id=team_id).first()
    json = [
        {
            "id": comment.id,
            "create_date": comment.create_date,
            "author": comment.user.username,
            "team_id": comment.team.id,
            "team": comment.team.mascot,
            "comment": comment.comment,
        } for comment in  team.comments
    ]
    return jsonify({"comments": json})
