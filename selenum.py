from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import requests
import random
from fakemail import * 
from smsactivate.api import SMSActivateAPI
from os import getenv
import string
from fakemail import *
APIKEY = getenv("BOT_TOKEN")

def generate_password(length=12):
    lowercase_letters = string.ascii_lowercase
    uppercase_letters = string.ascii_uppercase
    digits = string.digits
    special_chars = string.punctuation
    all_chars = lowercase_letters + uppercase_letters + digits + special_chars
    password = ''.join(random.choice(all_chars) for _ in range(length))
    password_list = list(password)
    random.shuffle(password_list)
    password_list[0] = random.choice(lowercase_letters)
    password_list[1] = random.choice(uppercase_letters)
    password_list[2] = random.choice(digits)
    password_list[3] = random.choice(special_chars)
    password = ''.join(password_list)
    return password

def generate_nickname():
    first_names = ["Alex", "Emma", "Michael", "Sophia", "William", "Olivia", "Daniel", "Ava", "Matthew", "Isabella"]
    last_names = ["Smith", "Johnson", "Williams", "Jones", "Brown", "Davis", "Miller", "Wilson", "Moore", "Taylor"]
    suffixes = [str(random.randint(1000, 9999)) for _ in range(10)]

    first_name = random.choice(first_names)
    last_name = random.choice(last_names)
    suffix = random.choice(suffixes)

    return first_name,last_name
def getnumber():
    link=f'https://sms-activate.org/stubs/handler_api.php?api_key={APIKEY}&action=getNumber&service=ot&forward=0&country=0&maxPrice=10'
    req=requests.get(link)
    a=req.text.split(':')
    return a[1],a[2][1:]
def getStatus(id):
    link=f'https://api.sms-activate.org/stubs/handler_api.php?api_key={APIKEY}&action=getStatus&id={id}'
    req=requests.get(link)
    while(req.text=="STATUS_WAIT_CODE"):
        req=requests.get(link)
        time.sleep(0.5)
    return req.text.split(":")[2][1:]
def main():
    sa = SMSActivateAPI(APIKEY)
    if(float(sa.getBalance()['balance'])<=10.0):
        print("Додик пополни баланс")
        return 0
    s = Service(executable_path="./chromedriver.exe")
    driver = webdriver.Chrome(service=s)
    driver.get("https://driver.deliver.ru/bargains")
    time.sleep(6)
    id,num=getnumber()
    nomer=driver.find_element(By.XPATH, "//*[@id='app']/div/div/div[3]/div/div[2]/form/div[1]/input")
    nomer.send_keys(num)
    knopka1=driver.find_element(By.XPATH, "//*[@id='app']/div/div/div[3]/div/div[2]/form/span/button")
    knopka1.click()
    time.sleep(4)
    kod=driver.find_element(By.XPATH, "//*[@id='app']/div/div/div[3]/div/form/div[1]/input")
    kod.send_keys(getStatus(id))
    knopka2=driver.find_element(By.XPATH, "//*[@id='app']/div/div/div[3]/div/form/span/button")
    knopka2.click()
    time.sleep(6)
    first_name,last_name=generate_nickname()
    name1=driver.find_element(By.XPATH, "//*[@id='app']/div/div/div[3]/div/form/div[5]/div[1]/div[1]/input")
    name1.send_keys(first_name)
    name2=driver.find_element(By.XPATH, "//*[@id='app']/div/div/div[3]/div/form/div[5]/div[1]/div[2]/input")
    name2.send_keys(last_name)
    password=generate_password()
    pass1=driver.find_element(By.XPATH, "//*[@id='app']/div/div/div[3]/div/form/div[5]/div[2]/div/div[1]/input")
    pass1.send_keys(password)
    pass2=driver.find_element(By.XPATH, "//*[@id='app']/div/div/div[3]/div/form/div[5]/div[2]/div/div[2]/input")
    pass2.send_keys(password)
    inn=driver.find_element(By.XPATH, "//*[@id='app']/div/div/div[3]/div/form/div[5]/div[1]/div[4]/div[1]/div/div/div[1]/input")
    inn.send_keys("7734370287")
    knopka4=driver.find_element(By.XPATH, "//*[@id='app']/div/div/div[3]/div/form/div[8]/label")
    knopka4.click()
    knopka3=driver.find_element(By.XPATH, "//*[@id='app']/div/div/div[3]/div/form/div[9]/label")
    knopka3.click()
    #email_manager = TemporaryEmailManager()
    #email = email_manager.create_email(expiry_time=14)
    #emails = email_manager.get_emails(email)
    print("/////////////////////////////////////////////////////////////////")
    knopka5=driver.find_element(By.XPATH, "//*[@id='app']/div/div/div[3]/div/form/div[5]/div[1]/div[4]/div[1]/div")
    knopka5.click()
    time.sleep(1)
    print("/////////////////////////////////////////////////////////////////")
    dropdown_element = driver.find_element(By.XPATH, "//*[@id='app']/div/div/div[3]/div/form/div[5]/div[1]/div[4]/div[1]/div/ul/li")
    dropdown_element.click()
    email_manager = TemporaryEmailManager()
    emailadress=email_manager.create_email()
    milo=driver.find_element(By.XPATH, "//*[@id='app']/div/div/div[3]/div/form/div[5]/div[1]/div[3]/input")
    milo.send_keys(emailadress)
    knopka6=driver.find_element(By.XPATH, "//*[@id='app']/div/div/div[3]/div/form/div[10]/span/button")
    knopka6.click()
    time.sleep(2)
    milo2=driver.find_element(By.XPATH, "//*[@id='app']/div/div/div[3]/div/form/div[1]/input")
    milo2.send_keys(email_manager.getnum(emailadress))
    knopka6=driver.find_element(By.XPATH, "//*[@id='app']/div/div/div[3]/div/form/span/button")
    knopka6.click()
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        print("huy")
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        try:
            WebDriverWait(driver, 10).until(
                lambda driver: driver.execute_script("return document.body.scrollHeight") > last_height
            )
        except:
            break
        last_height = driver.execute_script("return document.body.scrollHeight")
    time.sleep(100)
    




if __name__=="__main__":
    main()
