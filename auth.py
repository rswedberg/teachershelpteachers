# Import python libraries
import json
import os
import sqlite3

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
from db_execute import User, Questions
from db import init_db_command


class Auth():
    """
    This class contains methods for a single sign-on for Google users. It
    redirects users to choose a Google account and returns with a id, name, email,
    and profile picture.
    """
    # Decleare constant variables
    GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID", None)
    GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET", None)
    GOOGLE_DISCOVERY_URL = (
        "https://accounts.google.com/.well-known/openid-configuration"
    )

    # User session management setup
    # https://flask-login.readthedocs.io/en/latest
    login_manager = LoginManager()

    # OAuth 2 client setup
    client = WebApplicationClient(GOOGLE_CLIENT_ID)


    def login(self):
        """
        This method operates the login route. It redirects the user to a Google
        interface to select the prefered Google account.
        @return redirect to request_uri
        """
        # Find out what URL to hit for Google login
        google_provider_cfg = requests.get(self.GOOGLE_DISCOVERY_URL).json()
        authorization_endpoint = google_provider_cfg["authorization_endpoint"]

        # Use library to construct the request for Google login and provide
        # scopes that let you retrieve user's profile from Google
        request_uri = self.client.prepare_request_uri(
            authorization_endpoint,
            redirect_uri=request.base_url + "/callback",
            scope=["openid", "email", "profile"],
        )
        return redirect(request_uri)

    
    def callback(self):
        """
        This method operates the login/callback route. It gathers user information
        from Google, stores it in a databse, and returns to the index route
        with a cookie session for the user.
        @return redirect to index route
        """
        # Get authorization code Google sent back to you
        code = request.args.get("code")
        # Find out what URL to hit to get tokens that allow to ask for
        # things on behalf of a user
        google_provider_cfg = requests.get(self.GOOGLE_DISCOVERY_URL).json()
        token_endpoint = google_provider_cfg["token_endpoint"]
        # Prepare and send a request to get tokens
        token_url, headers, body = self.client.prepare_token_request(
            token_endpoint,
            authorization_response=request.url,
            redirect_url=request.base_url,
            code=code
        )
        token_response = requests.post(
            token_url,
            headers=headers,
            data=body,
            auth=(self.GOOGLE_CLIENT_ID, self.GOOGLE_CLIENT_SECRET),
        )

        # Parse the tokens!
        self.client.parse_request_body_response(json.dumps(token_response.json()))
        # Find and hit the URL from Google that gives the user's profile
        # information, including their Google profile image and email
        userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
        uri, headers, body = self.client.add_token(userinfo_endpoint)
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

    
    def logout():
        """
        This method logs the user out by clearing the session cookie and returning
        to the index route.
        """
        logout_user()
        return redirect("/")
