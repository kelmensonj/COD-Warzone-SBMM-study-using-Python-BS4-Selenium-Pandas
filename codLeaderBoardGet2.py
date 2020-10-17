from concurrent.futures import ThreadPoolExecutor
from bs4 import BeautifulSoup 
import pandas
import requests
import time
import os
import re
import datetime



MAX_THREADS = 30
INTERNET = True
LIST_DF = []
PAGE_LIMIT = False
PLATFORM = ['atvi', 'xbl', 'psn', 'battlenet']
REGION = ['us', 'ca']



def initiateDataframe():
	rows_data = []
	x = pandas.DataFrame(rows_data, COLUMNS)
	x.to_csv('xX_COD_LEADERBOARD_Xx.csv')

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
	global PAGE_LIMIT
	rows_data = []
	while INTERNET == False:
		try:
			print('bad internet')
			requests.get("http://google.com")
			INTERNET = True
		except:
			time.sleep(3)
			print('waited')
	try:
		page = requests.get(url)
		soup = BeautifulSoup(page.content)
		table_rows = soup.find_all('tr')
		if len(table_rows) == 0:
			PAGE_LIMIT = True
		else:
			pass
		for tr in table_rows[1:]:
			td = tr.find_all('td')
			row = [i.text for i in td]
			row = [i.replace('\n', ' ').replace('\r', '').replace(' ', '') for i in row]
			row[2] = url
			rows_data.append(row)
		

	except:
		INTERNET = False
		print('URL unreached, possibly iffy connection')
		
	leaderboard_page = pandas.DataFrame(rows_data, columns = ['Rank', 'Player', 'K/D', 'Matches'])
	LIST_DF.append(leaderboard_page)
	print(LIST_DF.index(leaderboard_page))
	if datetime.datetime.now().minutes % 15 == 0:
		saveData()
	else:
		pass
	
def saveData():
	global LIST_DF
	master = pandas.concat(LIST_DF)
	cols = [c for c in master.columns if c.lower()[:4] != 'unna']
	master=master[cols]
	master.to_csv('xX_COD_LEADERBOARD_Xx.csv')
	print('Saved File')
		

def main():
	global PLATFORM
	global REGION
	list_url = ['https://cod.tracker.gg/warzone/leaderboards/stats/' + j + '/KdRatio?country=' + k + '&page=' + str(i) for i in range(1,750,50) for j in PLATFORM for k in REGION]
	while PAGE_LIMIT == False:
		urlExecutor(list_url) 
		
	saveData()
	
	
main()
