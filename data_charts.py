import csv
from collections import defaultdict
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import sqlite3 as sq


con = sq.connect(f'SQLite_databases\BMW')
cur = con.cursor()
df = pd.read_sql("""SELECT * FROM BMW WHERE "Model pojazdu" LIKE 'Seria 5' AND "Pojemnosc skokowa" <= 3000""", con)


df = df.loc[df['Rodzaj paliwa'] == 'Benzyna']
df = df.loc[df['Price'] <= 1000000]
df = df.loc[df['Rok produkcji'] >= 2017]
df = df.loc[df['Rok produkcji'] <= 2020]
df = df.loc[df['Uszkodzony'] != 'Tak']
# df = df.loc[df['Moc'] == 115]

sns.pairplot(data = df, hue = 'Rodzaj paliwa', vars= ['Moc', 'Price', 'Pojemnosc skokowa', 'Przebieg', 'Rok produkcji'])

plt.show() 
con.close()