#!/usr/bin/env python4
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


app = Flask(__name__, template_folder="./web/templates")
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://jay:pass@localhost:5432/itse2302"
# app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = "HALO"
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.login_view = "auth.login"
login_manager.login_message = "Please login to access the resource"
login_manager.init_app(app)

from .modles import User

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


from .web import auth_blueprint
from .web import profile_blueprint
from .web import main_blueprint

from .api import teams_blueprint
from .api import conferences_blueprint

app.register_blueprint(auth_blueprint)
app.register_blueprint(profile_blueprint)
app.register_blueprint(main_blueprint)

app.register_blueprint(teams_blueprint)
app.register_blueprint(conferences_blueprint)

