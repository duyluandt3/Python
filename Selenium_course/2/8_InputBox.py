from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
import time

# Get chrome driver
driver = webdriver.Chrome(executable_path="C:\Drivers\chromedriver_win32\chromedriver.exe")

# Get web driver
driver.get("https://fs2.formsite.com/meherpavan/form2/index.html?1537702596407")

# Find how many input box present in the web page
inputBox = driver.find_elements(By.CLASS_NAME, 'text_field')
print(len(inputBox))

# Check available of text box
status = driver.find_element(By.ID, "RESULT_TextField-1").is_enabled()
if (status):
    # Input value in the text box
    driver.find_element(By.ID, "RESULT_TextField-1").send_keys("Dao")  # First Name
else:
    driver.quit()

status = driver.find_element(By.ID, "RESULT_TextField-2").is_enabled()
if status:
    time.sleep(1)
    driver.find_element(By.ID, "RESULT_TextField-2").send_keys("Luan")  # Last Name
else:
    driver.quit()

status = driver.find_element(By.ID, "RESULT_TextField-3").is_enabled()
if status:
    time.sleep(1)
    driver.find_element(By.ID, "RESULT_TextField-3").send_keys("0123456789")
else:
    driver.quit()

status = driver.find_element(By.ID, "RESULT_TextField-4").is_enabled()
if status:
    time.sleep(1)
    driver.find_element(By.ID, "RESULT_TextField-4").send_keys("Japan")
else:
    driver.quit()

status = driver.find_element(By.ID, "RESULT_TextField-5").is_enabled()
if status:
    time.sleep(1)
    driver.find_element(By.ID, "RESULT_TextField-5").send_keys("Osaka")
else:
    driver.quit()

status = driver.find_element(By.ID, "RESULT_TextField-6").is_enabled()
if status:
    time.sleep(1)
    driver.find_element(By.ID, "RESULT_TextField-6").send_keys("thismail@gmail.com")
else:
    driver.quit()


# Choose Gender Button
status = driver.find_element_by_xpath("//*[@id='RESULT_RadioButton-7_0']").is_selected()
if not status:
    button = driver.find_element_by_xpath("//*[@id='RESULT_RadioButton-7_0']")
    driver.execute_script("arguments[0].click();", button)
else:
    pass

# Choose day
status = driver.find_element_by_xpath("//*[@id='RESULT_CheckBox-8_0']").is_selected()
if not status:
    button = driver.find_element_by_xpath("//*[@id='RESULT_CheckBox-8_0']")
    driver.execute_script("arguments[0].click();", button)

# Select option drop down
select_element = driver.find_element(By.ID, "RESULT_RadioButton-9")
select_object = Select(select_element)
select_object.select_by_value('Radio-0')

# Print how many option
print(len(select_object.options))

# Click submit button
driver.find_element(By.ID, "FSsubmit").click()

time.sleep(5)
driver.quit()
