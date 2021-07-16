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
from db_execute import User, Questions
from db import init_db_command
# Configuration
GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID", None)
GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET", None)
GOOGLE_DISCOVERY_URL = (
    "https://accounts.google.com/.well-known/openid-configuration"
)

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
        raw_question = request.form.get("code")
        # Create a sample randomized question for user to view
        if request.form.get("action") == "view":

            sample = generateQuestion(raw_question)
            return render_template("create.html", sample=sample, category=category, raw_question=raw_question)
            # Separate string with | delimeter into list

            '''
            question = raw_question.split('|')
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
            return render_template("create.html", sample=sample, category=category, raw_question=raw_question)
        # Store question list into database
        '''
        else:
            # Get user
            user = current_user.email
            # Store to database
            Questions.create(user, category, raw_question)
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
@app.route("/retrieve", methods=["GET", "POST"])
def retrieve():
    # TODO
    if request.method == "GET":
        # retrieving questions from database
        return render_template("retrieve.html")
    else:
        # POST
        #questions = get_from_category("selection")
        author = request.form.get("author")
        category = request.form.get("category")
        try:
            numQs = int(request.form.get("numQs"))
        except:
            numQs = 1

        if author != "" and category != "":
            data = Questions.get_from_both(author, category)
        elif author != "":
            data = Questions.get_from_author(author)
        elif category != "":
            data = Questions.get_from_category(category)
        else:
            data = Questions.get()

        questions = ""
        for i in range(numQs):
            randomIndex = random.randint(0, len(data)-1)
            item = data[randomIndex]
            questions += generateQuestion(item[0]) + "\n^^^^^^^\n"
        #questions = [data[0], str(data), type(data), len(data)]


        return render_template("retrieve.html", questions=questions)



'''
Instructions:
-Write your question template followed by a triple dash ---
-You can create parameters that will have randomized values
by writing @ + capital letters starting with A
-parameters can be integers, floats, or strings
-After the triple dash, on separate lines and in order list
the letter, datatype, and other customization in the following
format (upper and lower bounds are inclusive)

Integers - letter, int, lowerbound, upperbound
Floats - letter, float, # of decimal values, lowerbound, upperbound
Strings - letter, str, item1, item2, ...

Ex.
num = @A
if num @B @C:
    print("1")
else:
    print("2")
---
A, int, 1, 8
B, str, >, <, !=
C, float, 1, 0, 9.5
'''
def generateQuestion(template):
    #print(template)
    try:
        template = template.split("---")
        question = template[0]
        parameters = template[1].strip().split("\n")
        #print(parameters)
        randomVals = []
        for i in range(len(parameters)):
            currentParam = parameters[i].split(",")
            letter = currentParam[0].strip()
            datatype = currentParam[1].strip()
            #print(currentParam, letter, datatype)
            if datatype == "int":
                lower = int(currentParam[2])
                upper = int(currentParam[3])
                #print(lower, upper)
                randomNum = random.randint(lower, upper)
                randomVals.append(randomNum)
                #print(randomNum)
            elif datatype == "float":
                lower = float(currentParam[3])
                upper = float(currentParam[4])
                decimalPlaces = int(currentParam[2])
                randomNum = round(random.uniform(lower, upper), decimalPlaces)
                randomVals.append(randomNum)
            else:
                stringList = []
                for j in range(2, len(currentParam)):
                    stringList.append(currentParam[j].strip())
                #print(stringList)
                randomStr = random.choice(stringList)
                randomVals.append(randomStr)

        #replace parameter string with generated values
        for i in range(len(parameters)):
            index = question.find("@")
            if index == len(question) - 2:
                #account for case when @X is last two chars of string
                question = question[:index] + str(randomVals[i])
            else:
                question = question[:index] + str(randomVals[i]) + question[index+2:]

        return question
    except:
        return "Something went wrong with that question template!"

if __name__ == "__main__":
    app.run(ssl_context="adhoc")
