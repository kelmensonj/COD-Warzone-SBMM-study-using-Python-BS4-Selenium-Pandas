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
PLATFORM = ['atvi', 'xbl', 'psn', 'battlenet']
REGION = ['cr']
#REGION = ['us', 'ca']
LIST_URL = []
PAGE_LIMIT = False



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
			
def removeURL(url):
	global PAGE_LIMIT
	global LIST_URL
	url_string = url
	page = int(url_string.split("page=",1)[1])
	url_start = url_string.split("page=",1)[0]
	for i in LIST_URL:
		if (url_start in i)  and (int(i.split("page=",1)[1]) >= page):
			LIST_URL.remove(i)
			
def scrapeURL(url):
	print(url)
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
		soup = BeautifulSoup(page.content,features = 'lxml')
		table_rows = soup.find_all('tr')
		if len(table_rows) == 0:
			removeURL(url)
		else:
			pass
		for tr in table_rows[1:]:
			td = tr.find_all('td')
			row = [i.text for i in td]
			row = [i.replace('\n', ' ').replace('\r', '').replace(' ', '') for i in row]
			del row[2]
			rows_data.append(row)
		

	except:
		INTERNET = False
		print('URL unreached, possibly iffy connection')
		
	leaderboard_page = pandas.DataFrame(rows_data, columns = ['Rank', 'Player', 'K/D', 'Matches'])
	print(leaderboard_page)
	LIST_DF.append(leaderboard_page)
	print(LIST_DF.index(leaderboard_page))
	if datetime.datetime.now().minute % 10 == 0:
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
	global LIST_URL
	LIST_URL = ['https://cod.tracker.gg/warzone/leaderboards/battle-royale/' + j + '/KdRatio?country=' + k + '&page=' + str(i) for i in range(1,750) for j in PLATFORM for k in REGION]
	while PAGE_LIMIT == False:
		urlExecutor(LIST_URL) 
		
	saveData()
	
	
main()
