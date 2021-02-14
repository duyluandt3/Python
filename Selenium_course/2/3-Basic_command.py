from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

for i in range(5):
    driver = webdriver.Chrome(executable_path="C:\Drivers\chromedriver_win32\chromedriver.exe")
    #driver.get("http://demo.automationtesting.in/Windows.html")
    driver.get("https://www.youtube.com/watch?v=TreQ0aSao-8&ab_channel=Tu%E1%BA%A5nTi%E1%BB%81nT%E1%BB%89")

    # Return driver title
    print(driver.title)
    # Get current page
    print(driver.current_url)

    # Click on the button in web page
    #driver.find_element_by_xpath("//*[@id='Tabbed']/a/button").click()
    driver.find_element_by_xpath("//button[@aria-label='Play']").click()

    time.sleep(5)

    # Close currently chrome tab
    #driver.close()
    # Quit all tab of chrome
    driver.quit()

    print(i)