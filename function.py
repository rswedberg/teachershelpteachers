# Import python libraries
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
import requests

# Internal imports
from db_execute import User, Questions

"""
 This class is used to opperate the routes that create the questions
 to be stored by the users.
"""
class Create():
    """
    This method operates the post request for the create route.
    @return confirm.html file with no variables
    """
    def create_post(self):
        question = []
        category = request.form.get("category")
        raw_question = request.form.get("code")
        # Create a sample randomized question for user to view
        if request.form.get("action") == "view":

            sample = Generator.generateQuestion(raw_question)
            return render_template("create.html", sample=sample, category=category, raw_question=raw_question)
            # Separate string with | delimeter into list
        else:
            # Get user
            try:
                user = current_user.email
            except:
                user = 'test.email'
            # Store to database
            Questions.create(user, category, raw_question)
            return render_template("confirm.html")

"""
This class is used to opperate the routes that retrieve questions that have
been stored in the database by users.
"""
class Retrieve():
    """
    This method opperates a get request for the retrieve route.
    @return retrieve.html file with a list of categories
    """
    def retrieve_get(self):
        categories = Questions.get_categories()
        return render_template("retrieve.html", categories=categories)

    """
    This method opperates a post request for the retrieve route.
    @return retrieve.html files with a string of questions and a list of categories
    """
    def retrieve_post(self):
        # POST
        categories = Questions.get_categories()
        method = request.form.get("search_method")
        category = request.form.get("categories")
        author = request.form.get("author")
        data = []
        if method == 'category':
            if category == None:
                return render_template("errorpage.html")
            data = Questions.get_from_category(category)
        elif method == 'author':
            data = Questions.get_from_author(author)
            if data == None:
                return render_template("errorpage.html")
        else:
            if category == None:
                return render_template("errorpage.html")
            data = Questions.get_from_both(author, category)
            if data == None:
                return render_template("errorpage.html")
        try:
            numQs = int(request.form.get("numQs"))
        except:
            numQs = 1
        questions = ""
        for i in range(numQs):
            randomIndex = random.randint(0, len(data)-1)
            item = data[randomIndex]
            questions += Generator.generateQuestion(item[0]) + "\n^^^^^^^\n"
        #questions = [data[0], str(data), type(data), len(data)]
        return render_template("retrieve.html", questions=questions, categories=categories)

"""
This class contains a method that generates questions with random values
from questions in their raw format and parameters for the variables.
"""
class Generator():
    """
    This method takes a string that contains a template for a raw question. The
    template must contain @ to identify variables for randomness, --- to
    separate the template from the paramters, and parameters for each identified
    variable. The method replaces the random variables with values that adhere
    to the parameters and stores it as a string. The method has the capability
    to make any number of the same type of question with different values for
    each random variable.
    @param string of question template
    @return string of completed questions
    """
    def generateQuestion(template):
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
