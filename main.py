import all_data_class as s
import csv
from datetime import date

today = date.today()
model_name = 'BMW_f20_seria1'
folder = 'BMW_f20_seria1'
link = 'https://www.otomoto.pl/osobowe/bmw/seria-1/od-2015?search%5Bfilter_enum_generation%5D=gen-f20-2011&search%5Border%5D=filter_float_price%3Aasc'

with open(f'C:\\Users\\tom19\VScode_Projects\\OTOmoto_project\\data\\{folder}\\{model_name}_{today}.csv', 'w', newline='') as cs_f:
            csv_title_list = ['Oferta od', 'Marka pojazdu', 'Price',  'Wersja', 'Model pojazdu', 'Generacja', 'Rok produkcji', 'Przebieg', 'Pojemnosc skokowa',
                            'Rodzaj paliwa', 'Moc', 'Skrzynia biegow', 'Naped', 'Liczba drzwi', 'Kolor', 'Bezwypadkowy', 'id']
            writer = csv.DictWriter(cs_f, fieldnames=csv_title_list)
            writer.writeheader()

            mercedes = s.Scraping(f'{link}', f'{model_name}', '&')
            mercedes.get_href()            
            for index, i in enumerate(mercedes.http_id[1]):
                a = mercedes.scrap_inner_info(i, mercedes.http_id[0][index])
                if a == None:
                    print('brak')
                    continue
                print(f'{round((index+1)/len(mercedes.http_id[1])*100, 2)}%----------{index}') # scraping progress %
                writer.writerow(mercedes.split_data(a[0], a[1])) 
                #https://www.otomoto.pl/oferta/bmw-seria-1-bardzo-ladna-salon-polska-oryginal-lakier-bez-wkladu-ID6F9DR1.html 64