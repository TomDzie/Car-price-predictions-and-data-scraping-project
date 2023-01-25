import csv
from collections import defaultdict
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_csv('data\BMW_f20_seria1\database_BMW_f20_seria1.csv')
# df = df.loc[df['Rodzaj paliwa'] == 'Benzyna']
# df = df.loc[df['Pojemnosc skokowa'] > 1800]
df = df.loc[df['Uszkodzony'] == 'Tak']

sns.pairplot(data = df, hue = 'Rodzaj paliwa', vars= ['Price', 'Pojemnosc skokowa', 'Przebieg', 'Rok produkcji'])

plt.show() 
