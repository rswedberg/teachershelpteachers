from flask_login import UserMixin
from collections import OrderedDict

from db import get_db

"""
This class contains calls to the user table in the databse. Objects of this
class contain the attributes of id, name, email, and profile picture.
"""
class User(UserMixin):
    """
    This constructor instatiates a User with an id, name, email, and profile
    picture.
    @param user id
    @param user name
    @param user email
    @param user profile picture
    """
    def __init__(self, id_, name, email, profile_pic):
        self.id = id_
        self.name = name
        self.email = email
        self.profile_pic = profile_pic

    """
    This static method uses the user id to return all the attributes of a
    user object that were saved in a databse.
    @param user id
    @return user object attributes
    """
    @staticmethod
    def get(user_id):
        db = get_db()
        user = db.execute(
            "SELECT * FROM user WHERE id = ?", (user_id,)
        ).fetchone()
        if not user:
            return None

        user = User(
            id_=user[0], name=user[1], email=user[2], profile_pic=user[3]
        )
        return user

    """
    This static method creates a new row in a database for all four attribtues
    of the user object.
    @param user id
    @param user name
    @param user email
    @param user profile picture
    """
    @staticmethod
    def create(id_, name, email, profile_pic):
        db = get_db()
        db.execute(
            "INSERT INTO user (id, name, email, profile_pic) "
            "VALUES (?, ?, ?, ?)",
            (id_, name, email, profile_pic),
        )
        db.commit()

"""
This class contains calls to the questions table in the database.
"""
class Questions():
    """
    This static method searches the database for the category provided in the
    parameter. It then returns the question attribute for the category.
    @param string category
    @return string question
    """
    @staticmethod
    def get_from_category(category):
        db = get_db()
        question = db.execute(
            "SELECT question FROM questions WHERE category = ?", (category,)
        ).fetchall()
        if not question:
            return None
        return question

    """
    This static method searches the databse for the author provided in the
    paramter. It then returns the question attribute for the author.
    @param string author email
    @return string question
    """
    @staticmethod
    def get_from_author(author):
        db = get_db()
        question = db.execute(
            "SELECT question FROM questions WHERE author = ?", (author,)
        ).fetchall()
        if not question:
            return None
        return question

    """
    This static method searches the databse for rows that contain both the
    author and the category provided by the paramters. It then returns the
    question attribute that matches the search.
    @param string author email
    @param string category
    @return string question
    """
    @staticmethod
    def get_from_both(author, category):
        db = get_db()
        question = db.execute(
            "SELECT question FROM questions WHERE author = ? AND category = ?", (author, category)
        ).fetchall()
        if not question:
            return None
        return question

    """
    This static method creates a list of all the categories in the database.
    @return list of string categories
    """
    def get_categories():
        db = get_db()
        db_call = db.execute(
            "SELECT category FROM questions"
        ).fetchall()
        list = []
        for i in range(len(db_call)):
            cat = db_call[i]
            list.append(cat[0])
        raw_cat = OrderedDict.fromkeys(list)
        category = sorted(raw_cat, key = lambda s: s.casefold())
        if not category:
            return None
        return category

    """
    This static method creates a new row in the databse for all of the question
    attributes including the author's email, category, and question in its
    raw form.
    @param string author email
    @param string category
    @param string question 
    """
    @staticmethod
    def create(author, category, question):
        db = get_db()
        db.execute(
            "INSERT INTO questions (author, category, question) "
            "VALUES (?, ?, ?)", (author, category, question)
        )
        db.commit()
