import sqlite3 as sq
import csv



con = sq.connect(f'directory.db')
cur = con.cursor()
cur.execute(f"""CREATE TABLE BMW
                ("Oferta od" VARCHAR(30),"Marka pojazdu" VARCHAR(30),"Price" NUMBER,"Data" DATE,"Wersja" VARCHAR(30),"Model pojazdu" VARCHAR(30),
                 "Generacja" VARCHAR(30),"Rok produkcji" NUMBER(4),"Przebieg" NUMBER(10),"Pojemnosc skokowa" NUMBER(5),"Rodzaj paliwa" VARCHAR(30),"Moc" NUMBER,
                 "Skrzynia biegow" VARCHAR(30),"Naped" VARCHAR(30),"Liczba drzwi"NUMBER,"Kolor" VARCHAR(30),"Bezwypadkowy" VARCHAR(30),"Uszkodzony" VARCHAR(30),"id" NUMBER PRIMARY KEY)""")
con.commit()
con.close()

#append DB with csv data

with open("data\\BMW_f20_seria1\\database_BMW_f20_seria1.csv", "r", newline="") as daily:
    daily_reader = csv.reader(daily)
    row_index = None
    con = sq.connect(f'directory.db')
    cur = con.cursor()
    for index, row in enumerate(daily_reader):
        cur.execute(f"""INSERT INTO BMW VALUES {tuple(row)}""")
        print(index)
        con.commit()
con.close()