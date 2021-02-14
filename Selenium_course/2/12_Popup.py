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