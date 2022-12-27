import requests
from bs4 import BeautifulSoup
import csv

class Scraping():
    def __init__(self, http, model, http_extention):
        self.http = http
        self.model = model
        self.http_extention = http_extention
        self.http_id = [[], []]
        self.number_of_pages = 0
    

    @staticmethod
    def replace_polish(word):
        word.replace('ł', 'l').replace(
            'ż', 'z').replace('ó', 'o').replace('ś', 's').replace('ć', 'c').replace('ź', 'z').replace('Ł','L').replace(
            'Ż', 'Z').replace('Ó', 'O').replace('Ś', 'S').replace('Ć', 'C').replace('Ź', 'z').replace('ę','e').replace(
            'Ę', 'E').replace('ą', 'a').replace('Ą', 'A').replace('ń', '').replace('Ń', 'N')

    
    def get_href(self):
        a = 0
        
        offers_page = requests.get(self.http).text
        soup_offers_page = BeautifulSoup(offers_page, 'lxml')                           #soup main offer page
        self.number_of_pages = soup_offers_page.find_all(class_='ooa-xdlax9 ekxs86z0')       #gets number of pages to loop
        http1 = self.http
        if len(self.number_of_pages) == 0:                                                   #if there is one page only
            self.number_of_pages = 1
        else:
            self.number_of_pages = int(self.number_of_pages[-1].text)


        for i in range(self.number_of_pages):
            self.http = http1 + f'{self.http_extention}page={i+1}'
            offers_page = requests.get(self.http).text
            soup_offers_page = BeautifulSoup(offers_page, 'lxml')
            offers = soup_offers_page.find_all(attrs={'data-testid': "listing-ad"})     # all offers

            for index, offer in enumerate(offers):
                get_http = offer.find('a', href=True).get('href')                       #get refs
                self.http_id[1].append(get_http)
                id = offer.get('id')                                                    #get offer id
                self.http_id[0].append(id)                
                print(f'{a + 1}: {id}, {get_http}')                                     #for testing
                a+=1
    @staticmethod            
    def scrap_inner_info(ref_link, id):
        label_list = []
        value_list = []
        offers_page = requests.get(ref_link).text
        soup_offers_page = BeautifulSoup(offers_page, 'lxml')
        if len(soup_offers_page.find_all(class_ = 'offer-price changeFinanceLinkOrder')) == 0:
            return None
        price = soup_offers_page.find(class_='offer-price changeFinanceLinkOrder').get('data-price')
        params__label = soup_offers_page.find_all(class_='offer-params__label')  # title of parameter
        params__value = soup_offers_page.find_all(class_='offer-params__value')  # value of parameter
        for i in range(len(params__value)):
            params__label_ready = params__label[i].text.replace('\n', '').replace('  ', '').replace('ł', 'l').replace(
                'ż', 'z').replace('ó', 'o').replace('ś', 's').replace('ć', 'c').replace('ź', 'z').replace('Ł','L').replace(
                'Ż', 'Z').replace('Ó', 'O').replace('Ś', 'S').replace('Ć', 'C').replace('Ź', 'z').replace('ę','e').replace(
                'Ę', 'E').replace('ą', 'a').replace('Ą', 'A').replace('ń', '').replace('Ń', 'N')
            params__value_ready = params__value[i].text.replace('\n', '').replace('  ', '').replace('ł', 'l').replace(
                'ż', 'z').replace('ó', 'o').replace('ś', 's').replace('ć', 'c').replace('ź', 'z').replace('Ł','L').replace(
                'Ż', 'Z').replace('Ó', 'O').replace('Ś', 'S').replace('Ć', 'C').replace('Ź', 'z').replace('ę','e').replace(
                'Ę', 'E').replace('ą', 'a').replace('Ą', 'A').replace('ń', '').replace('Ń', 'N')
            label_list.append(params__label_ready)
            value_list.append(params__value_ready)
        label_list.append('Price')
        value_list.append(price)
        label_list.append('id')
        value_list.append(id)
        return label_list, value_list

    @staticmethod
    def split_data(label_list1, value_list1):
        values = []
        csv_title_list = ['Oferta od', 'Marka pojazdu', 'Price',  'Wersja', 'Model pojazdu', 'Generacja', 'Rok produkcji', 'Przebieg', 'Pojemnosc skokowa',
                            'Rodzaj paliwa', 'Moc', 'Skrzynia biegow', 'Naped', 'Liczba drzwi', 'Kolor', 'Bezwypadkowy', 'id']
        for i, parameter in enumerate(csv_title_list):
            if parameter in label_list1:
                value = value_list1[label_list1.index(parameter)]
            elif parameter not in label_list1:
                value = '0'

            values.append(
                value.replace('ł', 'l').replace(
                'ż', 'z').replace('ó', 'o').replace('ś', 's').replace('ć', 'c').replace('ź', 'z').replace('Ł','L').replace(
                'Ż', 'Z').replace('Ó', 'O').replace('Ś', 'S').replace('Ć', 'C').replace('Ź', 'z').replace('ę','e').replace(
                'Ę', 'E').replace('ą', 'a').replace('Ą', 'A').replace('ń', '').replace('Ń', 'N'))
        dict_values = {'Oferta od': values[0], 'Marka pojazdu': values[1],'Price': values[2], 'Wersja': values[3], 'Model pojazdu': values[4],
                    'Generacja': values[5],
                    'Rok produkcji': values[6], 'Przebieg': values[7], 'Pojemnosc skokowa': values[8],
                    'Rodzaj paliwa': values[9], 'Moc': values[10],
                    'Skrzynia biegow': values[11], 'Naped': values[12], 'Liczba drzwi': values[13], 'Kolor': values[14],
                    'Bezwypadkowy': values[15], 'id': values[16]}
        return dict_values

    @staticmethod
    def useless():
        print('pies')
