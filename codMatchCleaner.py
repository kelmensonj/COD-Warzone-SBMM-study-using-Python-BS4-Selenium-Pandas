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
PLATFORM = ['atvi', 'xbl', 'psn']
#REGION = ['cr']
#REGION = ['us', 'ca']
CHECKLIST = []
LIST_URL = []
SAVE_TIMER = 0

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
	global PLATFORM #####this this go to index of last row from loaded fully searched data, and begin iteration there
	global LIST_KDS
	global LIST_URL
	#global CHECKLIST
	for i in db:
		leaderboard_player = i[0]
		for match in i[1:]:
			match_num = i.index(match)
			for player in match:
				if ' ' not in player:
					for platform in PLATFORM:
						player_in_lobby = "https://cod.tracker.gg/warzone/profile/" + platform + "/" + player + "/overview"
						LIST_URL.append([player_in_lobby, [leaderboard_player, match_num]])
			
	new_list_url = []			
	df = findLeads()
	player_in_lobby_list = df['Lobby Player URL'].tolist()
	unique_leads = df['Leaderboard Player'].unique()
	LIST_URL = LIST_URL[100000:500000] + LIST_URL[2000000:2500000]
	for i in LIST_URL: ####this needs to be updated each timeKJkjfndewnvdnsoisd glitch on 100k to 500k, but got 0 to 100k entire^^above one line
		print(LIST_URL.index(i))
		if (i[1][0] in unique_leads) and (i[0] not in player_in_lobby_list):
			new_list_url.append(i)

	print(len(new_list_url))
			
			
	for start in range(0,len(new_list_url),10000):
		urlExecutor(new_list_url[start:start+10000])
		print("Recent start iterator: " + str(start))
		saveData(LIST_KDS)
		
		
		'''				
	player_in_lobby_list = checkIfSearched()
	for i in player_in_lobby_list			
	new_list_url = []
	today_search = []
	#
	sub_list = []
	for i in LIST_URL:
		sub_list.append(i[0])
		
	last_searched_profile_index_list
	for i in range(len(player_in_lobby_list)):
		last_searched_profile_index = sub_list.index(player_in_lobby_list[i])
		last_searched_profile_index_list.append(last_searched_profile_index)
	maximum_index = max(last_searched_profile_index_list)
	LIST_URL = LIST_URL[maximum_index+1:]
	for x in range(1000):
		new_list_url = []
		for i in LIST_URL:
			new_list_url = []
			if (len(new_list_url)<10000) and i not in today_search:
			
		
	#
	for start in range(0,len(LIST_URL)):
		new_list_url = []
		for i in range(start,len(LIST_URL)): 
			if (LIST_URL[i][0] not in player_in_lobby_list) and (len(new_list_url) < 10000) and (LIST_URL[i] not in today_search) :
				new_list_url.append(LIST_URL[i])
				today_search.append(LIST_URL[i])
				print('unsearched')
			else:
				print('duplicate')
				pass
		print("Found " + str(len(LIST_KDS)) + " rows")
		urlExecutor(new_list_url)
		saveData(LIST_KDS)
	
			'''
			
def urlExecutor(list_url):
	urls = []
	references = []
	for individual_player_object in list_url:
		urls.append(individual_player_object[0])
		references.append(individual_player_object[1])	
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
					#print('waited')

			executor.map(scrapeURL, urls, references)
			
def scrapeURL(url, reference):
	global INTERNET
	global LIST_KDS
	global SAVE_TIMER
	while INTERNET == False:
		try:
			#print('bad internet')
			requests.get("http://google.com")
			INTERNET = True
		except:
			time.sleep(3)
			#print('waited')
	try:
		page = requests.get(url)
		soup = BeautifulSoup(page.content,features = 'lxml')
		mydivs = soup.findAll("span", {"class": "value"})
		kd = mydivs[2].text
		leaderboard_player = reference[0]
		match_num = reference[1]
		LIST_KDS.append([leaderboard_player,match_num,kd,url,mydivs])
	except:
		INTERNET = False
		pass

	
	
	
def saveData(list_kds):
	global SAVE_TIMER
	df = pandas.DataFrame(list_kds, columns = ['Leaderboard Player', 'Match #', 'K/D of Lobby Player', 'Lobby Player URL','Other Data'])
	df.to_csv('xX_COD_MATCH_FATSO15_Xx.csv')   #######hereherehereherehereheekjdbvskdjbvksdbvksjbvksbkjvbskjdbvskbvjks#########################################################3
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
	
def checkIfSearched():
	player_in_lobby_list = []
	for i in range(1,30):
		try:
			df = pandas.read_csv('xX_COD_MATCH_FATSO' + str(i) + '_Xx.csv')
			df_list = df['Lobby Player URL'].tolist()
			for player in df_list:
				player_in_lobby_list.append(player)
		except:
			pass
	return player_in_lobby_list
	
def findLeads():
	df_list = []
	for i in range(1,30):
		try:
			df = pandas.read_csv('xX_COD_MATCH_FATSO' + str(i) + '_Xx.csv')
			df_list.append(df)
		except:
			pass
	df = pandas.concat(df_list)
	return df
	
def main():
	#getCHECKLIST()
	db = matchCleaner()
	initiateDataframe(db)
	
	
main()




		

		
		
		

	

