import pandas

df1 = pandas.read_csv('will_COD_data_BIG.csv')
df2 = pandas.read_csv('will_COD_data_LITTLE.csv')

records3 = df2.to_records(index=False)
result3 = list(records3)


'''records1 = df1.to_records(index=False)
result1 = list(records1)

records2 = df2.to_records(index=False)
result2 = list(records2)'''

df_means = pandas.DataFrame(df1.groupby('Leaderboard Player')['K/D of Lobby Player'].mean().reset_index()) 
df_count = pandas.DataFrame(df1.groupby('Leaderboard Player')['K/D of Lobby Player'].count().reset_index())

records1 = df_means.to_records(index=False)
result1 = list(records1)

records2 = df_count.to_records(index=False)
result2 = list(records2)

listo = []




for tup in result1:
	name = tup[0].split('/')[-2]
	appendage = []
	idx = result1.index(tup)
	appendage.append([tup,result2[idx]])
	for i in records3:
		if i[3] == name:
			appendage.append(i)
			
	name = appendage[1][3]
	kd = appendage[1][4]
	matches = appendage[1][5]
	url = appendage[0][0][0]
	avg_kd_ag = appendage[0][0][1]
	sample = appendage[0][1][1]
	listo.append([name,kd,matches,url,avg_kd_ag,sample])
	

df = pandas.DataFrame(listo, columns = ['Name','K/D','Matches','URL','AVG K/D AGAINST','SAMPLE'])  
df.to_csv('theDataCOD.csv')






