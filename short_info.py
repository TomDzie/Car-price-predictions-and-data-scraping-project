import requests
from bs4 import BeautifulSoup
import csv
a = 1
engines = [[
    [90, 125],
    [126, 160],
    [161, 200],
    [201, 280],
    [281, 329],
    [330, 500]
    ],
    [
    [80, 107],
    [108, 127],
    [128, 165],
    [166, 205],
    [206, 280]
    ]]

version_g = [[
    '116i',
    '118i',
    '120i',
    '125i',
    'M135i',
    'M140i'
    ],
    [
    '114d',
    '116d',
    '118d',
    '120d',
    '125d'
    ]]

ful = ['petrol', 'diesel']
with open('data1.csv', 'w', newline='') as cs_f:
    fieldnames = ['index', 'title', 'year', 'mileage', 'price', 'fuel', 'version', 'id']
    writer = csv.DictWriter(cs_f, fieldnames=fieldnames)
    writer.writeheader()
    for n in range(2):

        for j in range(len(engines[n])):
            main_page = requests.get(
                f'https://www.otomoto.pl/osobowe/bmw/seria-1/od-2015?search%5Bfilter_enum_generation%5D=gen-f20-2011&search%5Bfilter_enum_fuel_type%5D={ful[n]}&search%5Bfilter_float_engine_power%3Afrom%5D={engines[n][j][0]}&search%5Bfilter_float_engine_power%3Ato%5D={engines[n][j][1]}&search%5Border%5D=filter_float_price%3Aasc&search%5Badvanced_search_expanded%5D=true&page=1').text
            soup_main_page = BeautifulSoup(main_page, 'lxml')
            strony = soup_main_page.find_all(class_='ooa-xdlax9 ekxs86z0')
            if len(soup_main_page.find_all(class_='ooa-xdlax9 ekxs86z0')) == 0:
                len_pages = 1
            else:
                len_pages = int(strony[-1].text)

            for i in range(1, len_pages + 1):
                print({engines[n][j][0]}, {engines[n][j][1]})
                html_text = requests.get(
                    f'https://www.otomoto.pl/osobowe/bmw/seria-1/od-2015?search%5Bfilter_enum_generation%5D=gen-f20-2011&search%5Bfilter_enum_fuel_type%5D={ful[n]}&search%5Bfilter_float_engine_power%3Afrom%5D={engines[n][j][0]}&search%5Bfilter_float_engine_power%3Ato%5D={engines[n][j][1]}&search%5Border%5D=filter_float_price%3Aasc&search%5Badvanced_search_expanded%5D=true&page={i}').text
                soup = BeautifulSoup(html_text, 'lxml')
                offers1 = soup.find_all(attrs={'data-testid': "listing-ad"})  # all offers
                for index, offer in enumerate(offers1):
                    if 'EUR' in offer.find(class_='ooa-1bmnxg7 e1b25f6f11').text:
                        continue
                    id = offer.get('id')
                    title = offer.find(class_='e1b25f6f6 e1b25f6f20 ooa-10p8u4x er34gjf0').text  # offer title
                    price = offer.find(class_='ooa-1bmnxg7 e1b25f6f11').text  # Price
                    if 'Niski' in offer.find_all(class_='ooa-1k7nwcr e1teo0cs0')[0].text:
                        year = offer.find_all(class_='ooa-1k7nwcr e1teo0cs0')[1].text  # Year
                    else:
                        year = offer.find_all(class_='ooa-1k7nwcr e1teo0cs0')[0].text  # Year
                    fuel = offer.find_all(class_='ooa-1k7nwcr e1teo0cs0')[-1].text  # fuel
                    mileage = offer.find_all(class_='ooa-1k7nwcr e1teo0cs0')[1].text #mileage
                    # if fuel == 'Diesel':
                    #     continue

                    writer.writerow({'index': a, 'title': title, 'year': year,'mileage': mileage, 'price': price, 'fuel': fuel,
                                     'version': version_g[n][j], 'id': id})

                    print(f'{a}: {title}, {price}, {year}, {fuel}, {mileage}, {id}') #6098474566
                    a += 1

