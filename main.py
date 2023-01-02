import all_data_class as s
import csv

mercedes = s.Scraping('https://www.otomoto.pl/osobowe/bmw/seria-1/od-2015?search%5Bfilter_enum_generation%5D=gen-f20-2011&search%5Border%5D=filter_float_price%3Aasc', 'BMW', '&')

mercedes.get_href()
model_name = ''
day = ''

with open('C:\\Users\\tom19\VScode_Projects\\OTOmoto_project\\data\\data.csv', 'w', newline='') as cs_f:
            csv_title_list = ['Oferta od', 'Marka pojazdu', 'Price',  'Wersja', 'Model pojazdu', 'Generacja', 'Rok produkcji', 'Przebieg', 'Pojemnosc skokowa',
                            'Rodzaj paliwa', 'Moc', 'Skrzynia biegow', 'Naped', 'Liczba drzwi', 'Kolor', 'Bezwypadkowy', 'id']
            writer = csv.DictWriter(cs_f, fieldnames=csv_title_list)
            writer.writeheader()            
            for index, i in enumerate(mercedes.http_id[1]):
                mercedes.scrap_inner_info(i, mercedes.http_id[0][index])

                if mercedes.scrap_inner_info(i, mercedes.http_id[0][index]) == None:
                    continue

                writer.writerow(mercedes.split_data(mercedes.scrap_inner_info(i, mercedes.http_id[0][index])[0], mercedes.scrap_inner_info(i, mercedes.http_id[0][index])[1])) 