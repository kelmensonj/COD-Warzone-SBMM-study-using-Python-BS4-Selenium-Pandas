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

MAX_THREADS = 2
INTERNET = True
LIST_DF = []
PATH = '/home/james/Downloads/chromedriver'


def getPlayerPlatform():
	df = pandas.read_csv('xX_COD_LEADERBOARD_Xx.csv')
	subset = df[['Player', 'URL']]
	player_platform_list = [tuple(x) for x in subset.to_numpy()]
	return player_platform_list
	
def transformURLS(player_platform_list):
	transformed_urls = []
	for player_platform in player_platform_list:
		player = player_platform[0]
		player = player.replace('#','%23',1)
		platform = player_platform[1].split("battle-royale/",1)[1].split("/Kd",1)[0]
		transformed_urls.append("https://cod.tracker.gg/warzone/profile/" + platform + "/" + player + "/matches")
	return transformed_urls
		
	

def urlExecutor(urls):
	global INTERNET
	print('urlExecutor')
	if len(urls) > 0:						
		print("Querying " + str(len(urls)) + " Pages for data")
		with ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:    
			while INTERNET == False:
				try:
					print('bad internet')
					requests.get("http://google.com")
					INTERNET = True
				except:
					time.sleep(3)
					print('waited')

			executor.map(scrapeURL, urls)
			
def scrapeURL(url):
	global INTERNET
	global LIST_DF
	global PATH
	row_data = []
	row_data.append(url)
	print(url)
	while INTERNET == False:
		try:
			print('bad internet')
			requests.get("http://google.com")
			INTERNET = True
		except:
			time.sleep(3)
			print('waited')
	try:
		driver = webdriver.Chrome(PATH)
		driver.get(url)
		
		for i in range(5):
			element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "match__link")))
			ps = driver.find_elements_by_class_name('match__link')
			element = ps[i]
			driver.execute_script("arguments[0].click()", element)
			element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "team__info")))
			content = driver.page_source
			soup = BeautifulSoup(content,'lxml')
			row_data.append(soup.text)
			driver.back()
		driver.close()
		

	except:
		INTERNET = False
		print('URL unreached, possibly iffy connection')
		
		
	row_data = [row_data]
	recent_match_page = pandas.DataFrame(row_data, columns = ['Player URL', 'Match 1', 'Match 2', 'Match 3', 'Match 4', 'Match 5'])
	LIST_DF.append(recent_match_page)
	if datetime.datetime.now().minutes % 15 == 0:
		saveData()
	else:
		pass
	print('SUCCESS!')
	
def saveData():
	global LIST_DF
	master = pandas.concat(LIST_DF)
	cols = [c for c in master.columns if c.lower()[:4] != 'unna']
	master=master[cols]
	master.to_csv('xX_COD_MATCHES_Xx.csv')
	print('Saved File')
		

def main():
	player_platform_list = getPlayerPlatform()
	recent_matches_urls = transformURLS(player_platform_list)
	narrowed_list = []
	for i in range(0,len(recent_matches_urls),20):
		narrowed_list.append(recent_matches_urls[i])	
	urlExecutor(narrowed_list)
	saveData()
	
	
main()


