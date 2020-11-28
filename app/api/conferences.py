from flask import Blueprint, request, Response, jsonify
from json import loads, dumps
from sqlalchemy import desc

from . import User, Conference, Team, Comment, Follow
from . import db

conferences = Blueprint("conferences", __name__, url_prefix="/api")

@conferences.route("/conferences")
def api_conferences():
    conferences = Conference.query.all()
    json = [
        {
            "id": conf.id,
            "name": conf.name,
            "short_name": conf.short_name,
            "abbreviation": conf.abbreviation,
            "teams": [
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
                } for team in conf.teams
            ],
        } for conf in conferences
    ]

    return jsonify({"conferences": json})

@conferences.route("/conferences/<conf_id>")
def api_single_conference(conf_id):
    conf = Conference.query.filter_by(id=conf_id).first()
    json = {
        "id": conf.id,
        "name": conf.name,
        "short_name": conf.short_name,
        "abbreviation": conf.abbreviation,
        "teams": [
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
            } for team in conf.teams
        ],
    }

    return jsonify({"conference": json})

