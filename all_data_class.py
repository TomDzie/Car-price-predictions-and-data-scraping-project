import requests
from bs4 import BeautifulSoup
import re

class Scraping():
    def __init__(self, http, model, http_extention):
        self.http = http
        self.model = model
        self.http_extention = http_extention
        self.http_id = [[], []]           #[0] -> id [1] -> url
        self.number_of_pages = 0
    

    def get_href(self):                #function scraping all offer's urls and IDs
        a = 0
        
        offers_page = requests.get(self.http).text                                         #requests page you chose
        soup_offers_page = BeautifulSoup(offers_page, 'lxml')                              #soup main offer page
        self.number_of_pages = soup_offers_page.find_all(class_='ooa-xdlax9 ekxs86z0')     #gets number of pages to loop
        http1 = self.http                                                                  #copy url
        if len(self.number_of_pages) == 0:                                                 #if there is one page only
            self.number_of_pages = 1
        else:
            self.number_of_pages = int(self.number_of_pages[-1].text)                      #-------


        for i in range(self.number_of_pages):                                              #go througth every pages loop
            self.http = http1 + f'{self.http_extention}page={i+1}'                         #adds page number to url
            offers_page = requests.get(self.http).text                                     #request specyfic offers page
            soup_offers_page = BeautifulSoup(offers_page, 'lxml')                          #scraping
            offers = soup_offers_page.find_all(attrs={'data-testid': "listing-ad"})        #finding all offers current page

            for index, offer in enumerate(offers):                                         #go througth every offer
                get_http = offer.find('a', href=True).get('href')                          #finding offer's url
                self.http_id[1].append(get_http)                                           #appending list with url
                id = offer.get('id')                                                       #finding offer's id
                self.http_id[0].append(id)                                                 #appending list with id
                print(f'{a + 1}: {id}, {get_http}')                                        #checking response
                a+=1                                                                       #for indexing
   
    @staticmethod            
    def scrap_inner_info(ref_link, id):                                                    #function for scrapping all offer's inner data
        label_list = []                                                                    #parameter title
        value_list = []                                                                    #parameter value
        offers_p = requests.get(ref_link, allow_redirects=False)                           #request specyfic offer's page
        if offers_p.status_code == 301:                                                    #check for redirecting to other site
            return None                                          
            
        offers_page = offers_p.text                                                        #scraping
        soup_offers_page = BeautifulSoup(offers_page, 'lxml')
        if len(soup_offers_page.find_all(class_ = 'offer-price changeFinanceLinkOrder')) == 0:
            return None                                                                                      #check if page doesn't work
        price = soup_offers_page.find(class_='offer-price changeFinanceLinkOrder').get('data-price')         #scrapes price
        params__label = soup_offers_page.find_all(class_='offer-params__label')                              # title of parameter
        params__value = soup_offers_page.find_all(class_='offer-params__value')                              # value of parameter
        for i in range(len(params__value)):                                                                  # appending parameters loops
            params__label_ready = params__label[i].text.replace('\n', '').replace('  ', '').replace('ł', 'l').replace(
                'ż', 'z').replace('ó', 'o').replace('ś', 's').replace('ć', 'c').replace('ź', 'z').replace('Ł','L').replace(
                'Ż', 'Z').replace('Ó', 'O').replace('Ś', 'S').replace('Ć', 'C').replace('Ź', 'z').replace('ę','e').replace(
                'Ę', 'E').replace('ą', 'a').replace('Ą', 'A').replace('ń', '').replace('Ń', 'N')
            params__value_ready = params__value[i].text.replace('\n', '').replace('  ', '').replace('ł', 'l').replace(
                'ż', 'z').replace('ó', 'o').replace('ś', 's').replace('ć', 'c').replace('ź', 'z').replace('Ł','L').replace(
                'Ż', 'Z').replace('Ó', 'O').replace('Ś', 'S').replace('Ć', 'C').replace('Ź', 'z').replace('ę','e').replace(
                'Ę', 'E').replace('ą', 'a').replace('Ą', 'A').replace('ń', '').replace('Ń', 'N')
            label_list.append(params__label_ready)                
            value_list.append(params__value_ready)                                                         #appending clean data
        label_list.append('Price')
        value_list.append(price)
        label_list.append('id')
        value_list.append(id)
        return label_list, value_list

    @staticmethod
    def split_data(label_list1, value_list1):                                #preparing data for csv
        values = []
        csv_title_list = ['Oferta od', 'Marka pojazdu', 'Price',  'Wersja', 'Model pojazdu', 'Generacja', 'Rok produkcji', 'Przebieg', 'Pojemnosc skokowa',
                            'Rodzaj paliwa', 'Moc', 'Skrzynia biegow', 'Naped', 'Liczba drzwi', 'Kolor', 'Bezwypadkowy', 'id']    #csv all columns
        for i, parameter in enumerate(csv_title_list):                       #go throuhgt columns 
            if parameter in label_list1:                                     #if offer has exact parameter saves it 
                value = value_list1[label_list1.index(parameter)]
            elif parameter not in label_list1:
                value = '0'                                                  #if not, sets it to 0

            values.append(value.replace('ł', 'l').replace(
                'ż', 'z').replace('ó', 'o').replace('ś', 's').replace('ć', 'c').replace('ź', 'z').replace('Ł','L').replace(
                'Ż', 'Z').replace('Ó', 'O').replace('Ś', 'S').replace('Ć', 'C').replace('Ź', 'z').replace('ę','e').replace(
                'Ę', 'E').replace('ą', 'a').replace('Ą', 'A').replace('ń', '').replace('Ń', 'N'))        #replacing all polish leeters not supported by csv            

        f1 = lambda x: int(re.sub('[^0-9]','', x))                                                       #replace all non numeric characters 

        dict_values = {'Oferta od': values[0], 'Marka pojazdu': values[1],'Price': f1(values[2]), 'Wersja': values[3], 'Model pojazdu': values[4],
                    'Generacja': values[5],
                    'Rok produkcji': f1(values[6]), 'Przebieg': f1(values[7]), 'Pojemnosc skokowa': f1(values[8]),
                    'Rodzaj paliwa': values[9], 'Moc': values[10],
                    'Skrzynia biegow': values[11], 'Naped': values[12], 'Liczba drzwi': f1(values[13]), 'Kolor': values[14],
                    'Bezwypadkowy': values[15], 'id': values[16]}                                       #ready dict
        return dict_values
