from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

driver = webdriver.Chrome(executable_path="C:\Drivers\chromedriver_win32\chromedriver.exe")
# driver.get("http://automationpractice.com/index.php")
driver.get("http://demo.guru99.com/test/newtours/")

# Return driver title
print(driver.title)
# Get current page
print(driver.current_url)

time.sleep(5)
# Get user name
element_userName = driver.find_element_by_name("userName")

# print(element.is_displayed())

if (element_userName.is_displayed()):
    # print(element.is_displayed())
    # time.sleep(1)
    print("User Name - OK\n")
    # Add user name
    element_userName.send_keys("mercury")
else:
    print("Non User Name\n")
element_passWord = driver.find_element_by_name("password")
if (element_passWord.is_displayed()):
    print("Password - OK\n")
    # Add password
    # time.sleep(1)
    element_passWord.send_keys("mercury")
else:
    print("Non Password\n")

time.sleep(2)
# Login button click
driver.find_element_by_name("submit").click()

# Check login status
checkLogin = driver.find_element_by_xpath(
    "/html/body/div[2]/table/tbody/tr/td[2]/table/tbody/tr[2]/td/table/tbody/tr/td[1]/a")
if (checkLogin.is_displayed()):
    print("Log in OK")
    # Click on Flights menu
    # Check flight menu
    ret = driver.find_element_by_xpath(
        "/html/body/div[2]/table/tbody/tr/td[1]/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr[2]/td[2]/a")
    if ret.is_displayed():
        time.sleep(1)
        driver.find_element_by_xpath(
            "/html/body/div[2]/table/tbody/tr/td[1]/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr[2]/td[2]/a").click()
        # Check selected button
        round_trip = driver.find_element_by_css_selector("input[value=roundtrip]")
        one_trip = driver.find_element_by_css_selector("input[value=oneway]")
        if round_trip.is_selected():
            print("round trip rario is selected")
        elif one_trip.is_selected():
            print("oneway rario is selected")
        else:
            print("non radio button is selected")
    else:
        print("Cannot find flight menu")
else:
    print("Log in false")
    driver.quit()

# driver.find_element_by_xpath("/html/body/div/div[1]/header/div[2]/div/div/nav/div[1]/a").click()
time.sleep(5)
driver.quit()