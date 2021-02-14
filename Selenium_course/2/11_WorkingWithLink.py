#########################################
# How many link present
# Capture link
# Click on the links
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

# Get link
driver.get("http://demo.guru99.com/test/newtours/")

# Find tag name of all link
allLink = driver.find_elements(By.TAG_NAME, "a")
# Print how many link is available on the web
print(len(allLink))
# Print all name of link
for link in allLink:
    print(link.text)

# Click on link text
status = driver.find_element(By.LINK_TEXT, "REGISTER").is_displayed()
if status:
    driver.find_element(By.LINK_TEXT, "REGISTER").click()