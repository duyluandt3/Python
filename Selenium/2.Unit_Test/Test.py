from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import unittest
import HtmlTestRunner


class GoogleSearch(unittest.TestCase):

    @classmethod
    def setUpClass(cls):

        cls.setPath = 'Chrome'
        if cls.setPath == 'Chrome':
            cls.driver = webdriver.Chrome()
        else:
            cls.driver = webdriver.Ie()
        # Search in google
        cls.driver.set_page_load_timeout(10)
        cls.driver.maximize_window()

    def test_search_automation(self):
        # Access to google
        self.driver.get("http://google.com")
        # Find by name by google
        que = self.driver.find_element_by_name("q")
        que.send_keys("Automation step by step")
        time.sleep(2)
        # Click button
        que.send_keys(Keys.ARROW_DOWN)
        que.send_keys(Keys.ENTER)

    @classmethod
    def tearDownClass(cls):
        cls.driver.maximize_window()
        cls.driver.refresh()
        time.sleep(5)
        cls.driver.quit()


if __name__ == '__main__':
    unittest.main(testRunner=HtmlTestRunner.HTMLTestRunner(
        output='D:/DATA\Electronic/Electronic Study/Python/Selenium/2.Unit_Test'))
