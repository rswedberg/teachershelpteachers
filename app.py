import os
import random
from flask import Flask, render_template, request, redirect

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template("index.html")
    else:
        if request.form.get("route") == "create":
            return redirect("/create")
        else:
            return redirect("/retrieve")

@app.route("/create", methods=["GET", "POST"])
def create():
    if request.method == "GET":
        return render_template("create.html")
    else:
        question = []
        if request.form.get("action") == "view":
            question = request.form.get("code").split('|')
            sample = ""
            for i in range(0,len(question)):
                if question[i] == "int":
                    sample += str(random.randint(1,9))
                else:
                    sample += question[i]
            return render_template("create.html", sample=sample)
        else:
            return render_template("confirm.html")

@app.route("/retrieve")
def retrieve():
    return render_template("retrieve.html")
