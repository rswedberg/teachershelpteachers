from db import get_db, close_db, init_db, init_db_command, init_app
from db_execute import User, Questions
from app import app, create_app, generateQuestion
import unittest

class TestUnit(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app_context = self.app.test_request_context()
        self.app_context.push()
        self.client = self.app.test_client(use_cookies=True)

    # Test create method for Questions table
    def test_questions_create(self):
        # Set values to be stored in database
        db_author = "author.email"
        db_category = "test category"
        db_question = "test question"
        # Call method to be tested
        Questions.create(db_author, db_category, db_question)
        # Initiate database to be called in current test
        db = get_db()
        # Test author value
        author = db.execute(
            "SELECT author FROM questions WHERE question = ?", (db_question,)
        ).fetchone()[0]
        self.assertEqual(db_author, author)
        # Test category value
        category = db.execute(
            "SELECT category FROM questions WHERE question = ?", (db_question,)
        ).fetchone()[0]
        self.assertEqual(db_category, category)
        # Test question value
        question = db.execute(
            "SELECT question FROM questions WHERE author = ?", (db_author,)
        ).fetchone()[0]
        self.assertEqual(db_question, question)
        # Clear test values from database
        db.execute(
            "DELETE FROM questions WHERE author = ?", (db_author,)
        )
        db.commit()

    def db_clear(self):
        db_category = "test question"
        db = get_db()
        db.execute(
            "DELETE FROM questions WHERE category = ?", (db_category,)
        )
        db.commit()


if __name__ == "__main__":
    unittest.main()
