# Python standard libraries
import os

# Third-party libraries
from flask import Flask, redirect, request, render_template
from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
)
from oauthlib.oauth2 import WebApplicationClient
import requests

# Internal imports
from db_execute import User
from auth import Auth
from function import Retrieve, Create

# Initialize Flask
def create_app():
    app = Flask(__name__, template_folder='templates', static_folder="static")
    return app
app = create_app()
app.secret_key = os.environ.get("SECRET_KEY") or os.urandom(24)

# User session management setup
# https://flask-login.readthedocs.io/en/latest
login_manager = LoginManager()
login_manager.init_app(app)

# Instantiate sub-classes
auth = Auth()
retrieve = Retrieve()
create = Create()

# Flask-Login helper to retrieve a user from the db
@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

# Home page that routes user to create page or retrieve page
@app.route("/", methods=["GET"])
def index():
    if current_user.is_authenticated:
        return render_template("index.html")
    else:
        return render_template("login.html")

# Create new question page
# Allow preview of sample question before storing question
@app.route("/create", methods=["GET", "POST"])
def dirver_create():
    if request.method == "GET":
        return render_template("create.html")
    else:
        return create.create_post()

@app.route("/login")
def driver_login():
    return auth.login()

@app.route("/login/callback")
def driver_callback():
    return auth.callback()

# Log user out
@app.route("/logout")
@login_required
def driver_logout():
    return auth.logout()

# Retrieve questions from databse
@app.route("/retrieve", methods=["GET", "POST"])
def driver_retrieve():
    if request.method == "GET":
        return retrieve.retrieve_get()
    else:
        return retrieve.retrieve_post()

if __name__ == "__main__":
    app.run(ssl_context="adhoc")
