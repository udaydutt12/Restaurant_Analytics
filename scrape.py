#!/usr/bin/env python3
from selenium import webdriver

class jellydash_bot:
    def __init__(self, info, driver = None):
        if driver is None:
            chrome_options = webdriver.ChromeOptions() 
            chrome_options.add_experimental_option("excludeSwitches", ['enable-automation'])
            self._driver = webdriver.Chrome(options=chrome_options)
        else:
            self._driver = driver
        self._email = info['email']
        self._password = info['password']
    def login(self):
        self._driver.get('https://www.toasttab.com/login')
        self._driver.find_element_by_id("email").send_keys(self._email)
        self._driver.find_element_by_id("password").send_keys(self._password)
        self._driver.find_element_by_id("log-in").click()  
    def execute(self):
        self.login()
        # write more code to execute here

if __name__=="__main__":
    # write your Toast username and password here
    user_info = {
        'email': 'bob@gmail.com',
        'password': '123456789'
    }
    bot = jellydash_bot(user_info)
    bot.execute()