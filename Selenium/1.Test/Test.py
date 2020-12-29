from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time


set = 'Chrome'
if set == 'Chrome':
    driver = webdriver.Chrome()
else:
    driver = webdriver.Ie()

# Search in google
driver.set_page_load_timeout(10)
# Access to google
driver.get("http://google.com")
# Find by name by google
que = driver.find_element_by_name("q")
que.send_keys("Automation step by step")
time.sleep(2)
# Click button
que.send_keys(Keys.ARROW_DOWN)
que.send_keys(Keys.ENTER)

driver.maximize_window()
driver.refresh()

time.sleep(5)

driver.quit()
