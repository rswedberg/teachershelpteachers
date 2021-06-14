# Python standard libraries
import json
import os
import sqlite3
import random
import re

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
from db import init_db_command
from user import User

# Configuration
GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID", None)
GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET", None)
GOOGLE_DISCOVERY_URL = (
    "https://accounts.google.com/.well-known/openid-configuration"
)

# Initialize Flask
app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY") or os.urandom(24)

# User session management setup
# https://flask-login.readthedocs.io/en/latest
login_manager = LoginManager()
login_manager.init_app(app)

# OAuth 2 client setup
client = WebApplicationClient(GOOGLE_CLIENT_ID)

# Flask-Login helper to retrieve a user from our db
@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

# Home page that routes user to create page or retrieve page
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        if current_user.is_authenticated:
            return render_template("index.html")
        else:
            return render_template("login.html")
    else:
        # Determine if user selects teh create button or the retrieve button
        if request.form.get("route") == "create":
            return redirect("/create")
        else:
            return redirect("/retrieve")

# Create new question page
# Allow preview of sample question before storing question
@app.route("/create", methods=["GET", "POST"])
def create():
    if request.method == "GET":
        return render_template("create.html")
    else:
        question = []
        category = request.form.get("category")
        # Create a sample randomized question for user to view
        if request.form.get("action") == "view":
            # Separate string with | delimeter into list
            question = request.form.get("code").split('|')
            sample = ""
            # Iterate through each string in list
            for i in range(0,len(question)):
                # Check for substring to idetify random integer
                if ("int" in question[i]
                and "{" in question[i]
                and "," in question[i]
                and "}" in question[i]):
                    # Separate substring to get minimum and maximum values
                    string = re.split('{|,|}', question[i])
                    minRange = int(string[1])
                    maxRange = int(string[2])
                    # Append random number in range to the sample question
                    sample += str(random.randint(minRange,maxRange))
                # Check for substring to identify random operator
                elif question[i] == "opp":
                    # List of operator options
                    opp = ['+', '-', '*', '/', '%']
                    # Append random operator to sample question
                    sample += opp[random.randint(0, len(opp)-1)]
                # Question components that are not to be randomized
                else:
                    # Append question component to sample question
                    sample += question[i]
            return render_template("create.html", sample=sample)
        # Store question list into database
        else:
            # TODO
            return render_template("confirm.html")

@app.route("/login")
def login():
    # Find out what URL to hit for Google login
    google_provider_cfg = requests.get(GOOGLE_DISCOVERY_URL).json()
    authorization_endpoint = google_provider_cfg["authorization_endpoint"]

    # Use library to construct the request for Google login and provide
    # scopes that let you retrieve user's profile from Google
    request_uri = client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri=request.base_url + "/callback",
        scope=["openid", "email", "profile"],
    )
    return redirect(request_uri)

@app.route("/login/callback")
def callback():
    # Get authorization code Google sent back to you
    code = request.args.get("code")
    # Find out what URL to hit to get tokens that allow to ask for
    # things on behalf of a user
    google_provider_cfg = requests.get(GOOGLE_DISCOVERY_URL).json()
    token_endpoint = google_provider_cfg["token_endpoint"]
    # Prepare and send a request to get tokens
    token_url, headers, body = client.prepare_token_request(
        token_endpoint,
        authorization_response=request.url,
        redirect_url=request.base_url,
        code=code
    )
    token_response = requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET),
    )

    # Parse the tokens!
    client.parse_request_body_response(json.dumps(token_response.json()))
    # Find and hit the URL from Google that gives the user's profile
    # information, including their Google profile image and email
    userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
    uri, headers, body = client.add_token(userinfo_endpoint)
    userinfo_response = requests.get(uri, headers=headers, data=body)
    # Make sure the email is verified.
    if userinfo_response.json().get("email_verified"):
        unique_id = userinfo_response.json()["sub"]
        users_email = userinfo_response.json()["email"]
        picture = userinfo_response.json()["picture"]
        users_name = userinfo_response.json()["given_name"]
    else:
        return "User email not available or not verified by Google.", 400
    # Create a user in db with the information provided by Google
    user = User(
        id_=unique_id, name=users_name, email=users_email, profile_pic=picture
    )

    # Doesn't exist? Add it to the database.
    if not User.get(unique_id):
        User.create(unique_id, users_name, users_email, picture)

    # Begin user session by logging the user in
    login_user(user)
    # Send user back to index (homepage)
    return redirect("/")

# Log user out
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/")

# Retrieve questions from databse
@app.route("/retrieve")
def retrieve():
    # TODO
    return render_template("retrieve.html")

if __name__ == "__main__":
    app.run(ssl_context="adhoc")
