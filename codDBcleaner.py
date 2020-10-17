import pandas

	
def concatDBs():
	df_list = []
	for i in range(1,30):
		try:
			df = pandas.read_csv('xX_COD_MATCH_FATSO' + str(i) + '_Xx.csv')
			df_list.append(df)
		except:
			pass
	df = pandas.concat(df_list)
	return df
	
def updateData(df):
	df['Leaderboard Player'] = df['Leaderboard Player'].str.replace('%23', '#')
	return df
	
def mergeData(df, df_leaders):
	df = pandas.merge(df,df_leaders, how='left',left_on=['Leaderboard Player'],right_on=['Player'])
	return df
	
def loadLeaders():
	df = pandas.read_csv('xX_COD_LEADERBOARD_Xx.csv')
	return df
	
def main():
	df = concatDBs()
	df = updateData(df)
	df.to_csv('will_COD_data_BIG.csv')
	df_leaders = loadLeaders()
	df_leaders.to_csv('will_COD_data_LITTLE.csv')
	#df = mergeData(df, df_leaders)
	#cols = [c for c in df.columns if c.lower()[:4] != 'unna']
	#df=df[cols]
	#df.to_csv('emailCODtry.csv')
	#print(df['K/D'])
	
	
	
main()
