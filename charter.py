import pandas
import matplotlib.pyplot as plt

'''df = pandas.read_csv('theDataCOD.csv')
print(df.columns)
print(df.head())
ax1 = df.plot.scatter(x='K/D', y='AVG K/D AGAINST', c='SAMPLE',colormap='viridis')
correlation = df.corr(method='pearson')
print(correlation)
#df.plot(x='K/D', y='AVG K/D AGAINST')
plt.show()'''

'''df = pandas.read_csv('theDataCOD.csv')
df = df.loc[df['SAMPLE'] > 100]
ax1 = df.plot.scatter(x='K/D', y='AVG K/D AGAINST', c='SAMPLE',colormap='viridis')
correlation = df.corr(method='pearson')
print(correlation)
plt.show()
plt.close()'''

df = pandas.read_csv('theDataCOD.csv')
df = df.loc[df['SAMPLE'] > 100]
df = df.loc[df['K/D'] < 10]
ax1 = df.plot.scatter(x='K/D', y='AVG K/D AGAINST', c='SAMPLE',colormap='viridis')
correlation = df.corr(method='pearson')
print(correlation)
plt.show()
plt.close()

df = pandas.read_csv('theDataCOD2.csv')
df = df.loc[df['SAMPLE'] > 30]
df = df.loc[df['K/D'] < 10]
ax1 = df.plot.scatter(x='K/D', y='AVG K/D AGAINST', c='SAMPLE',colormap='viridis')
correlation = df.corr(method='pearson')
print(correlation)
plt.show()
plt.close()
