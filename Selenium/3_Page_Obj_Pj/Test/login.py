import sys
import time
import unittest
from selenium import webdriver
import HtmlTestRunner

from homePage import HomePage
from loginPage import LoginPage


class LoginTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Get google extension
        cls.driver = webdriver.Chrome()
        cls.driver.implicitly_wait(10)
        # Set max size windows
        cls.driver.maximize_window()

    def test_login_valid(self):
        driver = self.driver
        driver.get("https://opensource-demo.orangehrmlive.com/")
        # Login page
        login = LoginPage(driver)
        login.enter_username("Admin")
        login.enter_password("admin123")
        time.sleep(2)
        login.click_login()

        # Access in homepage welcome
        homepage = HomePage(driver)
        time.sleep(2)
        homepage.click_welcome()
        time.sleep(2)
        homepage.click_logout()
        time.sleep(2)

        # Login this pages
        # self.driver.find_element_by_id("txtUsername").send_keys("Admin")
        # self.driver.find_element_by_id("txtPassword").send_keys("admin123")
        # time.sleep(2)
        # self.driver.find_element_by_id("btnLogin").click()
        # # Click on welcome
        # time.sleep(2)
        # self.driver.find_element_by_id("welcome").click()
        # # Logout
        # time.sleep(2)
        # self.driver.find_element_by_link_text("Logout").click()

    @classmethod
    def tearDownClass(cls):
        cls.driver.close()
        cls.driver.quit()
        print("Test Complete")


if __name__ == '__main__':
    unittest.main(testRunner=HtmlTestRunner.HTMLTestRunner(
        output='D:/DATAElectronic/Electronic Study/Python/Selenium/3_Page_Obj_Pj'))
