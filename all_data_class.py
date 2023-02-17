import requests
from bs4 import BeautifulSoup
import re
import csv
from datetime import date
import http.client
http.client._MAXHEADERS = 1000
import sqlite3 as sq


class Scraping:
    def __init__(self, http, http_extension):
        self.http = http
        self.http_extension = http_extension
        self.http_id = [[], []]  # [0] -> id [1] -> url
        self.number_of_pages = 0
        self.data = []

    def get_href(self):  # function scraping all offer's urls and IDs
        index = 0
        offers_page = requests.get(self.http).text  # requests page you chose
        soup_offers_page = BeautifulSoup(offers_page, "lxml")  # soup main offer page
        self.number_of_pages = soup_offers_page.find_all(
            class_="ooa-xdlax9 eesa4ha0")  # gets number of pages to loop
        http1 = self.http  # copy url
        if len(self.number_of_pages) == 0:  # if there is one page only
            self.number_of_pages = 1
        else:
            self.number_of_pages = int(self.number_of_pages[-1].text)

        for i in range(self.number_of_pages):  # go through every pages loop
            self.http = (
                http1 + f"{self.http_extension}page={i+1}")  # adds page number to url
            offers_page = requests.get(self.http).text  # request specific offers page
            soup_offers_page = BeautifulSoup(offers_page, "lxml")  # scraping
            offers = soup_offers_page.find_all(
                attrs={"data-testid": "listing-ad"})  # finding all offers current page
            print(f"page:{i+1}---------------{len(offers)} offers")

            for offer in offers:  # go through every offer
                get_http = offer.find("a", href=True).get("href")  # finding offer's url
                self.http_id[1].append(get_http)  # appending list with url
                id = offer.get("id")  # finding offer's id
                self.http_id[0].append(id)  # appending list with id
                print(f"{index + 1}: {id}, {get_http}")  # checking response
                index += 1  # for indexing

    @staticmethod
    def scrap_inner_info(ref_link, id):  # function for scrapping all offer's inner data
        label_list = []  # parameter title
        value_list = []  # parameter value
        today = date.today()
        offers_p = requests.get(ref_link, allow_redirects=False)  # request specific offer's page
        if offers_p.status_code == 301:  # check for redirecting to other site
            return None

        offers_page = offers_p.text  # scraping
        soup_offers_page = BeautifulSoup(offers_page, "lxml")
        if (len(soup_offers_page.find_all(class_="offer-price changeFinanceLinkOrder"))== 0):
            return None  # check if page doesn't work
        price = soup_offers_page.find(class_="offer-price changeFinanceLinkOrder").get(
            "data-price"
        )  # scrapes price
        params__label = soup_offers_page.find_all(
            class_="offer-params__label"
        )  # title of parameter
        params__value = soup_offers_page.find_all(
            class_="offer-params__value"
        )  # value of parameter
        for i in range(len(params__value)):  # appending parameters loops
            params__label_ready = remove_polish(
                params__label[i].text.replace("\n", "").replace("  ", "")
            )
            params__value_ready = remove_polish(
                params__value[i].text.replace("\n", "").replace("  ", "")
            )
            label_list.append(params__label_ready)
            value_list.append(params__value_ready)  # appending clean data
        label_list.append("Price")
        value_list.append(price)
        label_list.append("id")
        value_list.append(id)
        label_list.append("Data")
        value_list.append(f"{today}")
        return label_list, value_list


def remove_polish(text):
    text = (
        text.replace("ł", "l")
        .replace("ż", "z")
        .replace("ó", "o")
        .replace("ś", "s")
        .replace("ć", "c")
        .replace("ź", "z")
        .replace("Ł", "L")
        .replace("Ż", "Z")
        .replace("Ó", "O")
        .replace("Ś", "S")
        .replace("Ć", "C")
        .replace("Ź", "z")
        .replace("ę", "e")
        .replace("Ę", "E")
        .replace("ą", "a")
        .replace("Ą", "A")
        .replace("ń", "")
        .replace("Ń", "N")
    )
    return text


def data_to_dict(label_list1, value_list1, csv_title_list):  # preparing data for csv
    values = []
    for i, parameter in enumerate(csv_title_list):  # go throuhgt columns
        if parameter in label_list1:  # if offer has exact parameter saves it
            value = value_list1[label_list1.index(parameter)]
        elif parameter not in label_list1:
            value = "0"  # if not, sets it to 0

        values.append(
            remove_polish(value)
        )  # replacing all polish leeters not supported by csv

    f1 = lambda x: int(re.sub("[^0-9]", "", x))  # replace all non numeric characters
    f2 = lambda x: x[:-1] if len(x) > 1 else "0"  # replace last character
    dict_values = {
        "Oferta od": values[0],
        "Marka pojazdu": values[1],
        "Price": f1(values[2]),
        "Data": values[3],
        "Wersja": values[4],
        "Model pojazdu": values[5],
        "Generacja": values[6],
        "Rok produkcji": f1(values[7]),
        "Przebieg": f1(values[8]),
        "Pojemnosc skokowa": f1(f2(values[9])),
        "Rodzaj paliwa": values[10],
        "Moc": f1(values[11]),
        "Skrzynia biegow": values[12],
        "Naped": values[13],
        "Liczba drzwi": f1(values[14]),
        "Kolor": values[15],
        "Bezwypadkowy": values[16],
        "Uszkodzony": values[17],
        "id": values[18],
    }  # ready dict
    return dict_values


class scrape:
    def __init__(self, model_name: str, directory: str, url: str, http_extension: str):
        self.directory = directory
        self.model_name = model_name
        self.http_extension = http_extension
        self.url = url
        pass

    def csv(self):
        today = date.today()
        with open(
            f"{self.directory}\\{self.model_name}_{today}.csv", "w", newline=""
        ) as cs_f:
            csv_title_list = [
                "Oferta od",
                "Marka pojazdu",
                "Price",
                "Data",
                "Wersja",
                "Model pojazdu",
                "Generacja",
                "Rok produkcji",
                "Przebieg",
                "Pojemnosc skokowa",
                "Rodzaj paliwa",
                "Moc",
                "Skrzynia biegow",
                "Naped",
                "Liczba drzwi",
                "Kolor",
                "Bezwypadkowy",
                "Uszkodzony",
                "id",
            ]
            writer = csv.DictWriter(cs_f, fieldnames=csv_title_list)
            writer.writeheader()

            car = Scraping(f"{self.url}", self.http_extension)
            car.get_href()
            for index, i in enumerate(car.http_id[1]):
                a = car.scrap_inner_info(i, car.http_id[0][index])
                if a == None:
                    print("brak")
                    continue

                print(f"{round((index+1)/len(car.http_id[1])*100, 2)}%")  # scraping progress %
                writer.writerow(data_to_dict(a[0], a[1], csv_title_list))

    def SQlite(self, table_name):
        csv_title_list = [
            "Oferta od",
            "Marka pojazdu",
            "Price",
            "Data",
            "Wersja",
            "Model pojazdu",
            "Generacja",
            "Rok produkcji",
            "Przebieg",
            "Pojemnosc skokowa",
            "Rodzaj paliwa",
            "Moc",
            "Skrzynia biegow",
            "Naped",
            "Liczba drzwi",
            "Kolor",
            "Bezwypadkowy",
            "Uszkodzony",
            "id",
        ]

        car = Scraping(f"{self.url}", self.http_extension)
        car.get_href()
        con = sq.connect(f"{self.directory}")
        for index, i in enumerate(car.http_id[1]):
            cur = con.cursor()
            cur.execute(
                f"""SELECT COUNT(*) FROM {table_name} WHERE id = {car.http_id[0][index]}"""
            )

            if cur.fetchall()[0][0] >= 1:
                continue
            a = car.scrap_inner_info(i, car.http_id[0][index])
            if a == None:
                print("brak")
                continue

            data = data_to_dict(a[0], a[1], csv_title_list)

            cur.execute(
                f"""INSERT OR IGNORE INTO {table_name} VALUES
                            {tuple(data.values())}"""
            )
            con.commit()

            print(
                f"{round((index+1)/len(car.http_id[1])*100, 2)}%"
            )  # scraping progress %
        con.close()
