from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Get chrome driver
driver = webdriver.Chrome(executable_path="C:\Drivers\chromedriver_win32\chromedriver.exe")

# Wait to access
driver.implicitly_wait(5)

# Open maximum window size
driver.maximize_window()

# Get web page
# driver.get("https://www.expedia.com/")

driver.get("https://www.cleartrip.com/")
# Click on flight button
driver.find_element_by_xpath("/html/body/section[2]/div/aside[1]/nav/ul[1]/li[1]/a[1]").click()
time.sleep(2)

# Select Round Trip
driver.find_element(By.ID, "RoundTrip").click()

# From
driver.find_element(By.ID, "FromTag").send_keys("SFO")
# To
driver.find_element(By.ID, "ToTag").send_keys("NYC")

# Send From date
driver.find_element(By.ID, "DepartDate").clear()
driver.find_element(By.ID, "DepartDate").send_keys("15/2/2021")
# Send To date
driver.find_element(By.ID, "ReturnDate").clear()
driver.find_element(By.ID, "ReturnDate").send_keys("20/2/2021")

# Click some where on the page for go to next event
driver.find_element(By.XPATH, "//html").click()

# Wait to load page
time.sleep(1)
# Search Flight
driver.find_element(By.ID, "SearchBtn").click()

# Wait to load page
wait = WebDriverWait(driver, 10)

# Select Nonstop Button
# Wait to load all page
element = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='root']/div/main/div/div/div[1]/div/aside/div[4]/div[3]/div[2]/div/label[1]/div[1]/span")))
element.click()

time.sleep(5)

driver.quit()