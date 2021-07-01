from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import unittest

class GoogleSearchTest(unittest.TestCase):
    def setUp(self):
        #create a headless Chrome browser
        op = webdriver.ChromeOptions()
        op.add_argument('headless')

        self.driver = webdriver.Chrome("/Users/rkswedberg/Documents/Grad_School/Software_Engineering/Group_Project/teachersHelpTeachers/chromedriver", options=op)

    def test_int(self):
        # Get homepage
        self.driver.get("https://127.0.0.1:5000/")

        # Navigate through login
        # Click Google login
        self.driver.find_element_by_link_text("Google Login").click()
        # Wait 5 seconds to load Google accounts
        WebDriverWait(self.driver, 5)
        # Identify Google account
        self.driver.find_element_by_partial_link_text("rswedberg@unomaha.edu").click()
        # Wait 5 seconds to navigae back to application
        WebDriverWait(self.driver, 5)

        # Navigate to create question page
        self.driver.find_element_by_xpath("//button[1]").click()

        # Find textbox for entering questions and enter integer
        textbox = self.driver.find_element_by_name("code")
        textbox.clear()
        textbox.send_keys("num = |int{0,4}|")
        self.driver.find_element_by_xpath("//button[1]").click()

        # Read preview of question with random integer
        preview = self.driver.find_element_by_name("preview")
        print(preview.text)

    def tearDown(self):
        #close the browser window
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()
