from db import get_db, close_db, init_db, init_db_command, init_app
from db_execute import User, Questions
from app import app, create_app
from function import Generator
import unittest

class TestUnit(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app_context = self.app.test_request_context()
        self.app_context.push()
        self.client = self.app.test_client(use_cookies=True)
        # Send test values to questions table in databse to be retrieved in test methods
        self.author = "test.email"
        self.category = "test category"
        self.question = "test question"
        db = get_db()
        db.execute(
            "INSERT INTO questions (author, category, question) "
            "VALUES (?, ?, ?)", (self.author, self.category, self.question)
        )
        db.commit()

    # Test create method for Questions class
    def test_questions_create(self):
        # Call method to be tested
        Questions.create(self.author, self.category, self.question)
        # Initiate database to be called in current test
        db = get_db()
        # Test author value
        author = db.execute(
            "SELECT author FROM questions WHERE question = ?", (self.question,)
        ).fetchone()[0]
        self.assertEqual(self.author, author)
        # Test category value
        category = db.execute(
            "SELECT category FROM questions WHERE question = ?", (self.question,)
        ).fetchone()[0]
        self.assertEqual(self.category, category)
        # Test question value
        question = db.execute(
            "SELECT question FROM questions WHERE author = ?", (self.author,)
        ).fetchone()[0]
        self.assertEqual(self.question, question)

    # Test get_from_category method for Questions class
    def test_get_from_category(self):
        # Use method to get question from table using category
        data = Questions.get_from_category(self.category)
        value = data[0]
        string = value[0]
        # Test equality of question and the value from the database
        self.assertEqual(string, self.question)

    # Test get_from_author method for Questions class
    def test_get_from_author(self):
        # Use method to get question from table using author
        data = Questions.get_from_author(self.author)
        value = data[0]
        string = value[0]
        # Test equality of question and the value from the databse
        self.assertEqual(string, self.question)

    # Test get_from_both method for Questions class
    def test_get_from_both(self):
        # Use method to get question from table using author and category
        data = Questions.get_from_both(self.author, self.category)
        value = data[0]
        string = value[0]
        # Test equality of question and the value from the databse
        self.assertEqual(string, self.question)

    # Test get_categories method for Questions class
    def test_get_categories(self):
        # Use method to get list of categories from question table
        list = Questions.get_categories()
        # Test to make sure test category is in the list
        self.assertIn(self.category, list)
        # Test to make sure the list contains more than just test category
        self.assertNotEqual(self.category, list)

    # Test generateQuestion method for random integer in desired range
    def test_generateQuestion_int_in_range(self):
        # Minimum value in range
        min = 0
        # Maximum value in range
        max = 10
        # Create question template for min and max in range
        template = "@A---A, int, " + str(min) + ", " + str(max)
        # Iterate test 50 times to verify every random int is in range
        for i in range(0, 50):
            # Execute method to get a random int as a string in the full question
            randInt = int(Generator.generateQuestion(template))
            # Check if randInt is in the desired range
            self.assertIn(randInt, range(min, max + 1))

    # Test generateQuestion method for random float in desired range
    def test_generateQuestion_float_in_range(self):
        # Minimum value in range
        min = 0
        # Maximum value in range
        max = 10
        # Create question template for 1 decimal place in min and max range
        template = "@A---A, float, 1, " + str(min) + ", " + str(max)
        # Iterate test 50 times to verify every random float is the full question
        for i in range(0, 50):
            # Execute method to get a random float as a string in the full question
            randFloat = float(Generator.generateQuestion(template))
            # Check if randFloat is in the desired range
            self.assertLess(randFloat, max + 0.1)
            self.assertGreater(randFloat, min - 0.1)

    # Test generateQuestion method for random string in desired range
    def test_generateQuestion_str_in_range(self):
        # Define list of sample strings
        s = ['a', 'b', 'c', 'd']
        # Create question template for strings in list s
        template = "@A---A, str, " + s[0] + ", " + s[1] + ", " + s[2] + ", " + s[3]
        # Iterate test 50 times to verify every random string is in the list
        for i in range(0, 50):
            # Execute method to get a random string in the full question
            randStr = Generator.generateQuestion(template)
            # Check if randStr is in the list
            self.assertIn(randStr, s)

    # Test generateQuestion method for random negative integer in range
    def test_generateQuestion_int_negative(self):
        # Minimum value in range
        min = -10
        # Maximum value in range
        max = 0
        # Create question template for min and max in range
        template = "@A---A, int, " + str(min) + ", " + str(max)
        # Iterate test 50 times to verify every random int is in range
        for i in range(0, 50):
            # Execute method to get a random int as a string in the full question
            randInt = int(Generator.generateQuestion(template))
            # Check if randInt is in the desired range
            self.assertIn(randInt, range(min, max + 1))

    # Test generateQuestion method for random negative float in range
    def test_generateQuestion_float_negative(self):
        # Minimum value in range
        min = -10
        # Maximum value in range
        max = 0
        # Create question template for 1 decimal place in min and max range
        template = "@A---A, float, 1, " + str(min) + ", " + str(max)
        # Iterate test 50 times to verify every random float is the full question
        for i in range(0, 50):
            # Execute method to get a random float as a string in the full question
            randFloat = float(Generator.generateQuestion(template))
            # Check if randFloat is in the desired range
            self.assertLess(randFloat, max + 0.1)
            self.assertGreater(randFloat, min - 0.1)

    # Test generateQuestion method for true random int
    def test_generateQuestion_random_int(self):
        # Create question template for integer in 0 to 1000 range
        template = "@A---A, int, 0, 1000"
        # Get a sample int to test against other random ints
        baseInt = int(Generator.generateQuestion(template))
        # Set boolean value
        bool = False
        # Iterate to look for new int that is not equal to baseInt
        for i in range(0, 1000):
            if baseInt != int(Generator.generateQuestion(template)):
                # Change boolean value since new random int is different than base
                bool = True
        # Check if bool was changed to true
        self.assertTrue(bool)

    # Test generateQuestion method for true random float
    def test_generateQuestion_random_float(self):
        # Create question template for float in 0 to 1000 range
        template = "@A---A, float, 1, 0, 1000"
        # Get a sample float to test against other random floats
        baseFloat = float(Generator.generateQuestion(template))
        # Set boolean value
        bool = False
        # Iterate to look for new float that is not equal baseFloat
        for i in range(0, 1000):
            if baseFloat != float(Generator.generateQuestion(template)):
                # Change boolean value since new random float is different than base
                bool = True
        # Check if bool was changed to true
        self.assertTrue(bool)

    # Test generateQuestion method for true random string
    def test_generateQuestion_random_str(self):
        # Create question template for float in 0 to 1000 range
        template = "@A---A, str, a, b, c, d"
        # Get a sample string to test against other random strings
        baseStr = Generator.generateQuestion(template)
        # Set boolean value
        bool = False
        # Iterate to look for new string that is not equal baseStr
        for i in range(0, 1000):
            if baseStr != Generator.generateQuestion(template):
                # Change boolean value since new random str is different than base
                bool = True
        # Check if bool was changed to true
        self.assertTrue(bool)

    def tearDown(self):
        # Clear databse of test values in question table
        db = get_db()
        db.execute(
            "DELETE FROM questions WHERE category = ?", (self.category,)
        )
        db.commit()
        self.app_context.pop()

if __name__ == "__main__":
    unittest.main()
