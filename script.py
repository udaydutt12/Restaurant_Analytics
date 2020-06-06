#!/usr/bin/env python3
from selenium import webdriver
from time import sleep
from os import getcwd

chrome_options = webdriver.ChromeOptions() 
chrome_options.add_experimental_option("excludeSwitches", ['enable-automation'])
chrome_options.add_experimental_option("prefs", {"download.default_directory": getcwd()})
driver = webdriver.Chrome(options=chrome_options)
email = 'bob@gmail.com'
password = '123456789'
driver.get('https://www.toasttab.com/login')
driver.find_element_by_id("email").send_keys(email)
driver.find_element_by_id("password").send_keys(password)
sleep(2)
driver.find_element_by_id("log-in").click()
driver.get("https://www.toasttab.com/restaurants/admin/reports/home")
sleep(1)
driver.find_element_by_id("first-load-container").find_element_by_tag_name("button").click()
sleep(2)
summary_content = driver.find_element_by_id("sales-summary-content")
export_button = summary_content.find_element_by_css_selector('div a')
export_button.click()