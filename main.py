from parse import Parse
from manage_urls import ManagerURL
from manage_db import ManagerDB
from manage_text import ManagerText


class MainProgram:

    def __init__(self):
        self.p = Parse()
        self.m_url = ManagerURL()
        self.m_db = ManagerDB()
        self.m_t = ManagerText()

    def get_district(self) -> str:
        result = self.m_url.get_district_name()
        return result

    def set_url(self, name: str, url: str) -> tuple:
        change_name = self.m_t.change_name_district(
            name=name
        )

        result = self.m_url.add_url_to_json(
            name=name,
            url=url
        )
        return result

    def parsed_data(self) -> dict:
        result = self.p.get_data()

        return result

    def duplicate_checking(self, olx_id: int) -> bool:
        result = self.m_db.check_olx_id_exists(
            olx_id=olx_id
        )

        return result

    def get_week(self):
        data = self.m_db.get_recent_apartments()

        return data

    def get_month(self):
        data = self.m_db.get_recent_apartments(days=30)

        return data

    def get_clear_data(self) -> list:

        ans = []

        result = {
            'olx_id': [],
            'url': [],
            'price': [],
            'date': []
        }

        data = self.parsed_data()

        for i, id in enumerate(data['olx_id']):
            if not self.duplicate_checking(olx_id=id):
                result['olx_id'].append(data['olx_id'][i])
                result['url'].append(data['url'][i])
                result['price'].append(data['price'][i])
                result['date'].append(data['date'][i])

                self.m_db.add_apartment_to_db(
                    olx_id=data['olx_id'][i],
                    url=data['url'][i],
                    price=data['price'][i],
                    parsing_date=data['date'][i]
                )

        url = result['url']

        return url

    def get_district(self):
        result = self.m_url.get_district_name()

        return result
