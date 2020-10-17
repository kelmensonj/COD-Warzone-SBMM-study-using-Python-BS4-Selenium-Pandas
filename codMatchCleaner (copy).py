

from concurrent.futures import ThreadPoolExecutor
from bs4 import BeautifulSoup 
import pandas
import requests
import time
import os
import re
import datetime
import random



MAX_THREADS = 30
INTERNET = True
LIST_KDS = []
PLATFORM = ['atvi', 'xbl', 'psn', 'battlenet']
#REGION = ['cr']
#REGION = ['us', 'ca']
LIST_URL = []
PAGE_LIMIT = False
PLAYER = 'placeholder'
LIST_DF = []
DF = []
LIST_KDS = []
MATCH_NUM = 1
CHECKLIST = []

def getCHECKLIST():
	global CHECKLIST
	df = pandas.read_csv('xX_COD_MATCH_KDS_Xx.csv')
	player_list = df['Player'].tolist()
	for player in player_list:
		#player_split_url = player.split('/')
		#CHECKLIST.append(player_split_url[-2])
		CHECKLIST.append(player)
	print(CHECKLIST)

def initiateDataframe(db):
	global PLAYER
	global PLATFORM
	global MATCH_NUM
	global LIST_KDS
	global LIST_DF
	global CHECKLIST
	for i in db:
		player_player = i[0]
		if player_player not in CHECKLIST:
			row_data = []
			leaderboard_name = i[0]
			PLAYER = leaderboard_name
			row_data.append(PLAYER)
			print(PLAYER)
			for match in i[1:]:
				print(match)
				LIST_KDS = []
				MATCH_NUM = i.index(match)
				print("Match num " + str(MATCH_NUM))
				list_url = []
				for player in match:
					if ' ' not in player:
						for platform in PLATFORM:
							list_url.append("https://cod.tracker.gg/warzone/profile/" + platform + "/" + player + "/overview")
				print(list_url)
				urlExecutor(list_url)
				row_data.append(LIST_KDS)
			all_matches_per_player = pandas.DataFrame([row_data], columns = ['Player', 'Match 1', 'Match 2', 'Match 3', 'Match 4', 'Match 5'])
			LIST_DF.append(all_matches_per_player)
		if datetime.datetime.now().minute % 10 == 0:
			saveData()
			
			
def urlExecutor(urls):
	global INTERNET
	if len(urls) > 0:						
		#print("Querying " + str(len(urls)) + " Pages for data")
		with ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:    
			while INTERNET == False:
				try:
					#print('bad internet')
					requests.get("http://google.com")
					INTERNET = True
				except:
					time.sleep(3)
					print('waited')

			executor.map(scrapeURL, urls)
			
def scrapeURL(url):
	global INTERNET
	global LIST_KDS
	while INTERNET == False:
		try:
			#print('bad internet')
			requests.get("http://google.com")
			INTERNET = True
		except:
			time.sleep(3)
			print('waited')
	try:
		page = requests.get(url)
		soup = BeautifulSoup(page.content,features = 'lxml')
		mydivs = soup.findAll("span", {"class": "value"})
		LIST_KDS.append([mydivs[2].text,url])
		print('got a kd')
	except:
		INTERNET = False
		pass
	
def saveData():
	global LIST_DF
	master = pandas.concat(LIST_DF)
	cols = [c for c in master.columns if c.lower()[:4] != 'unna']
	master=master[cols]
	master.to_csv('xX_COD_MATCH_KDS_Xx.csv')
	print('Saved File')
	
def matchCleaner():
	df = pandas.read_csv('xX_COD_MATCHES_Xx.csv')
	subset = df[df.columns]
	tuples = [tuple(x) for x in subset.to_numpy()]
	#for row in tuples:
		#for match in row[2:]:
			#split_match = str.splitlines(match)
			#indices = [i for i, s in enumerate(split_match) if 'Kills' in s]
			#print(split_match[indices[0]].split('$3/mo',2)[2])
			#for i in indices[1:]:
				#print(split_match[i])
				#print('xxxx')
				
	#for row in tuples:
		#for match in row[2:]:
			#split_match = str.splitlines(match)
			#indices = [i for i, s in enumerate(split_match) if 'Kills' in s]
			#first = split_match[indices[0]]
			#first = first.split('/mo')
			#print('first')
			#print(first)
			#print('first')
			#for i in indices[1:]:
				#print(split_match[i])
				#print('xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx')
	master_list = []		
	for row in tuples:
		player_matches_list = []
		player_matches_list.append(row[1])
		for match in row[2:]:
			match_name_list = []
			match = match[match.index('1st'):match.index('Game materials copyright Activision')-397]
			#match_info_index = match.index('1/19/1970, 7:37:21 AM')
			#match_info = match[match_info_index-20:match_info_index+30]#this gets a substring that can be further analyzed in order to get the match number as well as the match type
			#match = match.split('         ')   
			#index_list_kills = [m.start() for m in re.finditer('Kills', match)]
			index_list_damage = [m.start() for m in re.finditer('Damage', match)]
			#for i in index_list_kills:
				#print(match[i:i+15])
			for i in index_list_damage:
				player_substring = match[i-80:i+15]
				x = '        '
				player_substring = player_substring.split(x,1)
				if player_substring[-1].count('Damage') > 1:
					player_substring[-1] = player_substring[-1][player_substring[-1].find('Damage')+15:]
				
				if len(player_substring[-1])>50:
					player_name = str.splitlines(player_substring[-1])[0]
					player_name = player_name.split(']', 1)[-1] 
					player_name = player_name.strip()
					match_name_list.append(player_name)
				
			player_matches_list.append(match_name_list)
		master_list.append(player_matches_list)
	return master_list
			

def main():
	#getCHECKLIST()
	db = matchCleaner()
	initiateDataframe(db)
	saveData()
	
	
main()




		

		
		
		

	

