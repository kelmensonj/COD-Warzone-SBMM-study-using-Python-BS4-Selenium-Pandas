from concurrent.futures import ThreadPoolExecutor
from bs4 import BeautifulSoup 
import pandas
import requests
import time
import datetime
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

PATH = '/home/james/Downloads/chromedriver'

def createAccount():
	url = 'https://s.activision.com/activision/registrationDetails?otherPlatform=ios'
	driver = webdriver.Chrome(PATH)
	driver.get(url)
		
	for i in range(200):
		time.sleep(10)
		el=driver.find_element_by_id("backdrop-register-full")
		action = webdriver.common.action_chains.ActionChains(driver)
		action.move_to_element_with_offset(el, 1, -300)
		action.click()
		action.perform()
		#ps = driver.find_elements_by_class_name('match__link')
		#element = ps[i]
		#driver.execute_script("arguments[0].click()", element)
		#element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "team__info")))
		#content = driver.page_source
		#soup = BeautifulSoup(content,'lxml')
		#row_data.append(soup.text)
		#driver.back()
		
def main():
	createAccount()
	
main()
