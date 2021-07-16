from flask_login import UserMixin

from db import get_db

class User(UserMixin):
    def __init__(self, id_, name, email, profile_pic):
        self.id = id_
        self.name = name
        self.email = email
        self.profile_pic = profile_pic

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

    @staticmethod
    def create(id_, name, email, profile_pic):
        db = get_db()
        db.execute(
            "INSERT INTO user (id, name, email, profile_pic) "
            "VALUES (?, ?, ?, ?)",
            (id_, name, email, profile_pic),
        )
        db.commit()

class Questions():
    @staticmethod
    def get_from_category(category):
        db = get_db()
        question = db.execute(
            "SELECT question FROM questions WHERE category = ?", (category,)
        ).fetchall()
        if not question:
            return None
        return question

    def get_from_author(author):
        db = get_db()
        question = db.execute(
            "SELECT question FROM questions WHERE author = ?", (author,)
        ).fetchall()
        if not question:
            return None
        return question

    def get_from_both(author, category):
        db = get_db()
        question = db.execute(
            "SELECT question FROM questions WHERE author = ? AND category = ?", (author, category)
        ).fetchall()
        if not question:
            return None
        return question

    def get_categories():
        db = get_db()
        email = "rswedberg@unomahae.edu"
        category = db.execute(
            "SELECT category FROM questions WHERE author = ?", (email)
        ).fetchall()
        if not category:
            return None
        return category

    def get():
        db = get_db()
        question = db.execute(
            "SELECT question FROM questions"
        ).fetchall()
        if not question:
            return None
        return question

    @staticmethod
    def create(author, category, question):
        db = get_db()
        db.execute(
            "INSERT INTO questions (author, category, question) "
            "VALUES (?, ?, ?)", (author, category, question)
        )
        db.commit()
