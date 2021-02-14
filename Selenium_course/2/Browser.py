from selenium import webdriver
from selenium.webdriver.common.keys import Keys

driver = webdriver.Chrome(executable_path="C:\Drivers\chromedriver_win32\chromedriver.exe")

driver.get("https://www.google.co.jp/")

# Title the page
print(driver.title)
# Return the URL the page
print(driver.current_url)
# Get HTML code
print(driver.page_source)

driver.close()