#########################################
# Click on popup
# Switch to Alert/ Popup
#########################################

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
import time

# Get chrome driver
driver = webdriver.Chrome(executable_path="C:\Drivers\chromedriver_win32\chromedriver.exe")

# Wait to access
driver.implicitly_wait(5)
# Get web page
driver.get("http://testautomationpractice.blogspot.com/")

driver.find_element_by_xpath("//*[@id='HTML9']/div[1]/button").click()

# Wait to load page
wait = WebDriverWait(driver, 5)

time.sleep(2)
# Click alert window using OK button
#driver.switch_to_alert().accept()

# Click cancel button
driver.switch_to_alert().dismiss()

