from bs4 import BeautifulSoup
import requests
from pyshorteners import Shortener
from datetime import datetime

from manage_urls import ManagerURL


class Parse:

    def __init__(self):
        self.manage_url = ManagerURL()
        self.tiny = Shortener()

    def get_data(self) -> dict:
        result = {
            'olx_id': [],
            'url': [],
            'price': [],
            'date': []
        }

        urls = self.manage_url.get_list_url()

        for url in urls:
            responce = requests.get(
                url=url
            )

            soup = BeautifulSoup(responce.text, 'lxml')

            main_div = soup.find(
                name='div',
                class_='css-j0t2x2'
            )

            room_data_div = main_div.find_all(
                name='div',
                class_='css-1sw7q4x'
            )

            list_of_id = [i.get('id') for i in main_div.find_all(
                name='div',
                class_="css-1sw7q4x"
            )]

            list_url = [self.tiny.tinyurl.short('https://www.olx.ua' + i.get('href')) for i in main_div.find_all(
                name='a',
                class_='css-z3gu2d'
            )][::2]

            list_price = [int(''.join(i.text.split('.')[0].split()[:-1])) for i in main_div.find_all(
                name='p',
                class_='css-13afqrm'
            )]

            parsing_date = datetime.now().date().strftime("%Y-%m-%d %H:00")

            n = len(list_price)

            list_date = [parsing_date] * n

            result['olx_id'] += list_of_id
            result['url'] += list_url
            result['price'] += list_price
            result['date'] += list_date

        return result
