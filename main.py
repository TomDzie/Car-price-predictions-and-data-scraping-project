import all_data_class as s
import csv
from datetime import date

model_name = 'BMW_f20_seria1'
url = 'https://www.otomoto.pl/osobowe/bmw/seria-1/od-2015?search%5Bfilter_enum_generation%5D=gen-f20-2011&search%5Border%5D=filter_float_price%3Aasc'
directory = 'C:\\Users\\tom19\VScode_Projects\\OTOmoto_project\\data\\BMW_f20_seria1'
directory1 = 'SQLite_databases\\BMW'

bmw = s.scrape(model_name, directory1, url)
bmw.SQlite('BMW')