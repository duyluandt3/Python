from selenium import  webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

driver = webdriver.Chrome(executable_path="C:\Drivers\chromedriver_win32\chromedriver.exe")

driver.get("https://seleniumhq.github.io/selenium/docs/api/java/index.html")

# Select frame mode
driver.find_element_by_xpath("/html/body/header/nav/div[1]/div[2]/ul[1]/li[1]/a").click()

time.sleep(3)
# Switch to frame
driver.switch_to.frame("packageListFrame")
# Get link in frame
driver.find_element_by_link_text("org.openqa.selenium").click()

# Switch to main frame
driver.switch_to.default_content()
time.sleep(3)
# Switch to package frame
driver.switch_to.frame("packageFrame")
# Click on WebDriver link
driver.find_element_by_link_text("WebDriver").click()

driver.switch_to.default_content()

time.sleep(3)
# Switch to class Frame
driver.switch_to.frame("classFrame")
driver.find_element_by_xpath("/html/body/header/nav/div[1]/div[1]/ul/li[6]/a").click()

time.sleep(5)

driver.quit()