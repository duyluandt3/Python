from selenium import webdriver
from selenium.webdriver.common.by import By
import time


driver = webdriver.Chrome(executable_path="C:\Drivers\chromedriver_win32\chromedriver.exe")

driver.get("http://demo.automationtesting.in/Windows.html")

# Click on click button
driver.find_element_by_xpath("//*[@id='Tabbed']/a/button").click()

# Print current windows
print(driver.current_window_handle) #print(driver.current_window_handle)

# Return all the handle value of opened browser windows
handles = driver.window_handles

for handle in handles:
    driver.switch_to.window(handle)
    print(driver.title)
    # Close parent window
    if driver.title == "Frames & windows":
        driver.close()

time.sleep(10)

driver.quit()