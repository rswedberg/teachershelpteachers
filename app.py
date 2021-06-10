import os
import random
import re
from flask import Flask, render_template, request, redirect

# Initialize Flask
app = Flask(__name__)

# Home page that routes users to create page or retrieve page
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template("index.html")
    else:
        # Determine if user selects the create button or the retrieve button
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
                # Check for substring to identify random integer
                if "int" and "{" and "," and "}" in question[i]:
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

# Retrieve questions from database
@app.route("/retrieve")
def retrieve():
    # TODO
    return render_template("retrieve.html")
