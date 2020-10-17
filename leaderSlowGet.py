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
#REGION = ['cr']
REGION = ['us', 'ca']
LIST_URL = []
PAGE_LIMIT = False




		
			
def removeURL(url):
	global LIST_URL
	url_string = url
	page = int(url_string.split("page=",1)[1])
	url_start = url_string.split("page=",1)[0]
	for i in LIST_URL:
		if (url_start in i)  and (int(i.split("page=",1)[1]) >= page):
			LIST_URL.remove(i)
			
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
		soup = BeautifulSoup(page.content,features = 'lxml')
		table_rows = soup.find_all('tr')
		if len(table_rows) == 0:
			PAGE_LIMIT = True
			removeURL(url)
			PAGE_LIMIT = False
		else:
			pass
		for tr in table_rows[1:]:
			td = tr.find_all('td')
			row = [i.text for i in td]
			row = [i.replace('\n', ' ').replace('\r', '').replace(' ', '') for i in row]
			del row[2]
			row.append(url)
			rows_data.append(row)
		

	except:
		INTERNET = False
		print('URL unreached, possibly iffy connection')
		
	leaderboard_page = pandas.DataFrame(rows_data, columns = ['Rank', 'Player', 'K/D', 'Matches', 'URL'])
	LIST_DF.append(leaderboard_page)
	if datetime.datetime.now().minute % 15 == 0:
		saveData()
	else:
		pass
	#if there are still players to rank
		#call executor on another interval higher of pages for the various regions
		#this way there are still lots of empty dataframes from empty pages with no players to rank, but there is still async and it will still just do around 30 url queries when theres no data
		#and then stop. So, check if theres that text, like if there are no rows check for that text, and if the text is there, dont call the next interval for the particular region and platform
		#so there would be no removing urls. the url list would be generated based on if theres data past the page
	
def saveData():
	global LIST_DF
	master = pandas.concat(LIST_DF)
	cols = [c for c in master.columns if c.lower()[:4] != 'unna']
	master=master[cols]
	master = master.drop_duplicates()
	master.to_csv('xX_COD_LEADERBOARD_Xx.csv')
	print('Saved File')
		

def main():
	ENDER = False
	global LIST_URL
	LIST_URL = ['https://cod.tracker.gg/warzone/leaderboards/battle-royale/' + j + '/KdRatio?country=' + k + '&page=' + str(i) for i in range(1,750) for j in PLATFORM for k in REGION]
	count = 0
	while PAGE_LIMIT == False and ENDER == False:
		for i in range(10000):
			print(i)
			try:
				url = LIST_URL[count]
				scrapeURL(url)
				count+=1
			except:
				ENDER = True
				pass
		
	saveData()
	
	
main()
