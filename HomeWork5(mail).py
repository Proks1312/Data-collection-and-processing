from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from pymongo import MongoClient

client = MongoClient('127.0.0.1', 27017)
db = client['data_mail']
email_list = db.massege
email_list.drop()

chrome_options = Options()
chrome_options.add_argument("start-maximized")
driver = webdriver.Chrome(executable_path='./chromedriver', options=chrome_options)
driver.implicitly_wait(15)

driver.get('https://account.mail.ru/')

elem_log = driver.find_element(By.XPATH, "//input[@name = 'username']")
elem_log.send_keys('study.ai_172@mail.ru')
elem_log.send_keys(Keys.ENTER)

elem_password = driver.find_element(By.XPATH, "//input[@name = 'password']")
elem_password.send_keys('NextPassword172#')
elem_password.send_keys(Keys.ENTER)

link_1_masseg = driver.find_element(By.XPATH, "//div[contains(@class, 'Grid__inner')]/a[1]").get_attribute('href')
driver.get(link_1_masseg)
while True:
    time.sleep(3)
    wait = WebDriverWait(driver, 5)
    content = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[contains(@id, 'BODY')]"))).get_attribute(
        'innerHTML')
    title = driver.find_element(By.XPATH, "//h2[@class = 'thread-subject']").text
    date = driver.find_element(By.XPATH, "//div[@class = 'letter__date']").text
    sender = driver.find_element(By.XPATH, "//div[@class='letter__author']/span[@class='letter-contact']").text
    try:
        db.massege.insert_one({
            'title': title,
            'date': date,
            'sender': sender,
            'link': driver.current_url
        })
    except:
        pass
    elem_button_next = driver.find_element(By.XPATH, "//span[contains(@class, 'arrow-down')]")
    if 'button2_disabled' in elem_button_next.get_attribute('class'):
        break
    elem_button_next.click()
driver.quit()
