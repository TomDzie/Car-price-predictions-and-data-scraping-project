import pandas as pd
import csv
from datetime import date
import re


def sort(directory: str, column_name: str or list):
    df = pd.read_csv(directory)
    df = df.sort_values(column_name)
    df.to_csv(directory, index= False)


def update_row(start, stop, id, data):
    pass

def add_column(directory:str, column_name:str, col_number:int = 0, value = None):
    df = pd.read_csv(directory)
    df.insert(col_number, column_name, value)
    df.to_csv(directory, index= False)


def delete_column(directory: str, column_name: str,):
    df = pd.read_csv(directory)
    df = df.drop(columns = column_name)
    df.to_csv(directory, index= False)


def delete_spaces():
    pass

def delete_letters():
    pass

def delete_phrase():
    pass

def type_int():
    pass

def change_format(directory: str, column: str, letters: bool = False, space: bool = False, letter: str = None, int: bool = False):
    df = pd.read_csv(directory) 
    for i in range(len(df[column].values)):

        if space == True:
            df[column].values[i] = df[column].values[i].replace(' ', '')

        if letters == True:
            f1 = lambda x: int(re.sub('[^0-9]','', x)) 
            df[column].values[i] = f1(df[column].values[i])

        if letter != None:
            df[column].values[i] = df[column].values[i].replace(f'{letter}', '')
        
        if int == True:
            try:
                df[column].values[i] = int(df[column].values[i])
            except ValueError:
                print('value not iterable')

    df.to_csv(directory, index= False)

def update_database(db_directory, directory_directory):
    daily_data_list = []
    daily_id = []
    with open(f'{directory_directory}', 'r', newline='') as daily:
        with open(f'{db_directory}', 'r+', newline='') as database:

            daily_reader = csv.reader(daily)
            database_reader = csv.reader(database)
            writer = csv.writer(database)
            row_index = None

            for row in daily_reader:
                daily_data_list.append(row)
                daily_id.append(row[-1])
            
            for row in database_reader:
                if row[-1] in daily_id:
                    row_index = daily_id.index(row[-1])                        
                    daily_id.remove(row[-1])
                    daily_data_list.remove(daily_data_list[row_index])
            for row in daily_data_list:
                writer.writerow(row)


def add_directory():
    pass

add_column('C:\\Users\\tom19\VScode_Projects\\OTOmoto_project\\data\\BMW_f20_seria1\\database_BMW_f20_seria1.csv', "Data", 3 , '2023.02.14')

# delete_column('C:\\Users\\tom19\VScode_Projects\\OTOmoto_project\\data\\BMW_f20_seria1\\database_BMW_f20_seria1.csv', "Data")