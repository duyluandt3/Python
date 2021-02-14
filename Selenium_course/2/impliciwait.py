import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

# Get driver
driver = webdriver.Chrome(executable_path="C:\Drivers\chromedriver_win32\chromedriver.exe")
# Get website page
driver.get("http://demo.guru99.com/test/newtours/")

# wait to find the site
driver.implicitly_wait(10)

# Check return title from web page
assert "Welcome: Mercury Tours" in driver.title

# Find and put username and password
driver.find_element_by_name("userName").send_keys("mercury")
time.sleep(1)
driver.find_element_by_name("password").send_keys("mercury")
# Click on submit
time.sleep(1)
driver.find_element_by_xpath("/html/body/div[2]/table/tbody/tr/td[1]/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr[2]/td[2]/a").click()
